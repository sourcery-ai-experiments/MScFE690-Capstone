import numpy as np
import pandas as pd
from bloomberg import BBG
from datetime import timedelta
from pandas.tseries.offsets import BDay, DateOffset
from calendars import DayCounts
from dateutil.relativedelta import relativedelta


class FwdIRSTrackers:
    """
    Class for creating excess return indices for rolling interest rate swaps using data from Bloomberg.
    At the start date, we assume we trade 100 notional 1M forward starting swaps with user-provided maturity.
    We mark-to-market the position over the month and then roll it into the new 1M forward at the end of the month.
    """

    currency_bbg_code_dict = {
        'AUD': 'AD', 'CAD': 'CD', 'CHF': 'SF', 'EUR': 'EU', 'GBP': 'BP',
        'JPY': 'JY', 'NZD': 'ND', 'SEK': 'SK', 'USD': 'US'
    }

    currency_calendar_dict = {
        'USD': DayCounts('30E/360 ISDA', calendar='us_trading'),
        'AUD': DayCounts('ACT/365', calendar='us_trading'),
        'CAD': DayCounts('ACT/365', calendar='us_trading'),
        'CHF': DayCounts('30A/360', calendar='us_trading'),
        'EUR': DayCounts('30U/360', calendar='us_trading'),
        'GBP': DayCounts('ACT/365', calendar='us_trading'),
        'JPY': DayCounts('ACT/365F', calendar='us_trading'),
        'NZD': DayCounts('ACT/365', calendar='us_trading'),
        'SEK': DayCounts('30A/360', calendar='us_trading')
    }

    def __init__(self, currency='USD', tenor=10, start_date='2004-01-05', end_date='today'):
        """
        Initializes FwdIRSTrackers object with specified parameters.

        :param currency: str, Currency symbol
        :param tenor: int, Tenor for the swap
        :param start_date: str, Start date for the tracker
        :param end_date: str, End date for the tracker
        """

        self.currency = currency
        self.tenor = tenor
        self.start_date = (pd.to_datetime(start_date) + BDay(1)).date()
        self.end_date = pd.to_datetime(end_date).date()
        self.day_count = self.currency_calendar_dict[currency]

        self.bbg = BBG()
        self.spot_swap_rates = self._get_spot_swap_rates()
        self.fwd_swap_rates = self._get_1m_fwd_swap_rates()
        self.df_tracker = self._calculate_excess_return_index()

        self.country = self.bbg.fetch_contract_parameter(self.ticker_spot, 'COUNTRY_ISO').iloc[0, 0].upper()
        self.exchange_symbol = self.bbg.fetch_contract_parameter(self.ticker_fwd, 'TICKER').iloc[0, 0]
        self.fh_ticker = 'irs ' + self.country.lower() + ' ' + self.currency.lower()

        self.df_metadata = pd.DataFrame(data={'fh_ticker': self.fh_ticker,
                                              'asset_class': 'fixed income',
                                              'type': 'swap',
                                              'currency': self.currency.upper(),
                                              'country': self.country.upper(),
                                              'maturity': self.tenor,
                                              'roll_method': '1 month'},
                                        index=[self.ticker_spot])

        self.df_tracker = self._get_melted_tracker_data()

    def _calculate_excess_return_index(self):
        """
        Calculate the excess return index based on spot and forward swap rates.

        :return: DataFrame, Excess return index
        """

        spot_rate_series = self.spot_swap_rates.iloc[:, 0].dropna()
        fwd_rate_series = self.fwd_swap_rates.iloc[:, 0].dropna()

        ts_df = pd.concat([spot_rate_series.to_frame('spot'), fwd_rate_series.to_frame('fwd_1m')],
                          axis=1, sort=True).fillna(method='ffill').dropna()

        er_index = pd.Series(index=ts_df.index)
        er_index.iloc[0] = 100

        start_date = er_index.index[0]
        fwd_swap_rate = ts_df.loc[start_date, 'fwd_1m'] / 100
        ref_swap_rate_d_minus_1 = fwd_swap_rate

        roll_date = self.day_count.busdateroll(start_date + relativedelta(months=1), 'modifiedfollowing')
        fwd_mat = self.day_count.busdateroll(start_date + relativedelta(months=1 + self.tenor * 12),
                                              'modifiedfollowing')

        for d in er_index.index[1:]:
            current_fwd_swap_rate = ts_df.loc[d, 'fwd_1m'] / 100
            current_spot_swap_rate = ts_df.loc[d, 'spot'] / 100
            curr_fwd_mat = self.day_count.busdateroll(d + relativedelta(months=1 + self.tenor * 12),
                                                       'modifiedfollowing')
            curr_spot_mat = self.day_count.busdateroll(d + relativedelta(months=self.tenor * 12),
                                                        'modifiedfollowing')

            w = 1 if d >= roll_date else self.day_count.tf(curr_fwd_mat, fwd_mat) / \
                                           self.day_count.tf(curr_fwd_mat, curr_spot_mat)

            ref_swap_rate = w * current_spot_swap_rate + (1 - w) * current_fwd_swap_rate

            pv01 = np.sum([(1 / 2) * ((1 + ref_swap_rate / 2) ** (-i)) for i in range(1, self.tenor * 2 + 1)])

            if np.isnan((ref_swap_rate_d_minus_1 - ref_swap_rate) * pv01):
                ret = 0
            else:
                ret = (ref_swap_rate_d_minus_1 - ref_swap_rate) * pv01

            er_index[d] = er_index[:d].iloc[-2] * (1 + ret)

            if d >= roll_date:
                roll_date = self.day_count.busdateroll(d + relativedelta(months=1), 'modifiedfollowing')
                fwd_mat = self.day_count.busdateroll(d + relativedelta(months=1 + self.tenor * 12),
                                                      'modifiedfollowing')
                ref_swap_rate_d_minus_1 = ts_df.loc[d, 'fwd_1m'] / 100
            else:
                ref_swap_rate_d_minus_1 = ref_swap_rate

        return er_index.to_frame('excess_return_index')

    def _get_spot_swap_rates(self):
        """
        Fetch spot swap rates data.

        :return: DataFrame, Spot swap rates
        """

        if self.currency == 'EUR':
            ticker = self.currency_bbg_code_dict[self.currency] + 'SA' + str(self.tenor) + ' Curncy'
        elif self.currency == 'NZD':
            ticker = self.currency_bbg_code_dict[self.currency] + 'SWAP' + str(self.tenor) + ' Curncy'
        else:
            ticker = self.currency_bbg_code_dict[self.currency] + 'SW' + str(self.tenor) + ' Curncy'

        bbg_raw_spot_data = self.bbg.fetch_series(securities=ticker,
                                                  fields='PX_LAST',
                                                  startdate=self.start_date,
                                                  enddate=self.end_date)

        self.ticker_spot = ticker

        bbg_raw_spot_data.columns = [self.currency + str(self.tenor) + 'Y']
        bbg_raw_spot_data.index = pd.to_datetime(bbg_raw_spot_data.index)

        return bbg_raw_spot_data.dropna(how='all')

    def _get_1m_fwd_swap_rates(self):
        """
        Fetch 1-month forward swap rates data.

        :return: DataFrame, 1-month forward swap rates
        """

        if self.currency == 'EUR':
            ticker = self.currency_bbg_code_dict[self.currency] + 'SAA' + str(self.tenor).zfill(2) + ' Curncy'
        elif self.currency == 'GBP':
            ticker = self.currency_bbg_code_dict[self.currency] + 'SWA' + str(self.tenor).zfill(2) + ' Curncy'
        elif self.currency == 'AUD':
            ticker = 'S0302FS 1M' + str(self.tenor) + 'Y BLC Curncy'
        elif self.currency == 'USD':
            ticker = self.currency_bbg_code_dict[self.currency] + 'FS0A' + str(self.tenor) + ' Curncy'
        else:
            ticker = self.currency_bbg_code_dict[self.currency] + 'FS0A' + str(self.tenor).zfill(2) + ' Curncy'

        bbg_fwd_data = self.bbg.fetch_series(securities=ticker,
                                             fields='PX_LAST',
                                             startdate=self.start_date,
                                             enddate=self.end_date)

        self.ticker_fwd = ticker

        bbg_fwd_data.columns = [self.currency + str(self.tenor) + 'Y']
        bbg_fwd_data.index = pd.to_datetime(bbg_fwd_data.index)

        return bbg_fwd_data.dropna(how='all')

    def _get_melted_tracker_data(self):
        """
        Get melted tracker data.

        :return: DataFrame, Melted tracker data
        """

        df = self.df_tracker[['excess_return_index']].rename({'excess_return_index': self.ticker_spot}, axis=1)
        df['time_stamp'] = df.index.to_series()
        df = df.melt(id_vars='time_stamp', var_name='fh_ticker', value_name='value')
        df = df.dropna()

        return df
