# interest rate hedging

class InterestRateSwap:
    """
    This class indicates the swap interest rate. This will be utilized to in derivative to manage interest rate.
    Attributes:
        principal: Is the swap principal and it is in floating.
        fixed_rate: It indicated the fixed interest rate and it is in floating.
        float_rate_ind: Indicate the floating rate index and it is string (LIBOR, SOFIA, SOFR).
        mat: Is the swap maturity in years and it is in integer.
    """
    def __init__(self, principal, fixed_rate, float_rate_ind, mat):
        self.principal = principal
        self.fixed_rate = fixed_rate
        self.float_rate_ind = float_rate_ind
        self.mat = mat

    def value(self):
        # This function will provide the swap value.
        # Encounting the pricipal and it will compare the current and fixed rate.
        pass

class InterestRateFuture:
    """
    This class indicate the future interest rate of the contact.
    Attributes:
        cont_size: This indicates the each contract size in terms of monetary valueand in this floating.
        set_price: This the settelment price that sttles the future contract and it is in floating. 
        mat: This is the maturity and provide the future expiration in years and it is in integer.
    """
    def __init__(self, cont_size, set_price, mat): 
        self.cont_size = cont_size
        self.set_price = set_price
        self.mat = mat

    def value(self):
        # This function will provide the futute value for the current market 
        # This can be found by evaluating the contract rate and current interate rate difference.
        pass

class InterestRateOption:
    """
    This class indicates the interest rates option.
    Attributes:
        strike_price (float): The set rate at which the option can be executed.
        premium (float): The cost to purchase the option.
        type (str): The type of option ('call' or 'put').
        maturity (int): The term of the option in years.
    """
    def __init__(self, str_price, prem, type, mat):
        self.str_price = str_price
        self.pre = pre
        self.type = type
        self.mat = mat

    def value(self):
        # This method should calculate the intrinsic value of the option.
        # For a call, it would be positive if current rates are above the strike; for a put, if below.
        pass

def assess_interest_rate_risk(current_rate, projected_rates):
    """
    Assess the potential risk due to changes in interest rates.
    Args:
        current_rate (float): The current interest rate.
        projected_rates (list of float): A list of projected future rates.
    Returns:
        float: The difference between the maximum and minimum projected rates as a measure of risk.
    """
    return max(projected_rates) - min(projected_rates)

def select_hedging_instrument(risk, instruments):
    """
    Selects a hedging instrument based on the assessed risk.
    Args:
        risk (float): The assessed risk level.
        instruments (list): A list of financial instruments available for hedging.
    Returns:
        list: A list of instruments deemed suitable for hedging given the risk.
    """
    if risk > 0.05:
        return [inst for inst in instruments if isinstance(inst, InterestRateSwap)]
    else:
        return [inst for inst in instruments if isinstance(inst, InterestRateOption)]
