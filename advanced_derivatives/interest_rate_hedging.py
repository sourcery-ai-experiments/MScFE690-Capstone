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
        str_price: This strike price, the option can be excersized at this rate and it is floating.
        pre: The premium is the price to purchase the option and it is floating.
        type: This is type which indicate the of option type, call or put and it is string.
        mat: This is the maturity and provide the option expiration in years and it is integer.
    """
    def __init__(self, str_price, prem, type, mat):
        self.str_price = str_price
        self.pre = pre
        self.type = type
        self.mat = mat

    def value(self):
        #This function will provide the option intrinsic value.
        # If the strike price are below the current rates it is indicating the call and if reverse it is inocating put.
        pass

def assess_interest_rate_risk(curr_rate, proj_rates):
    """
    This function evaluates any risk cuased by interest rate change
    Arguments:
        curr_rate: This is current rate and it is floating.
        proj_rates: This projected rate list and it is floating list.
    Returns:
        This is providing the maximum and minimum future rates difference, which it measures the risk and it is floating.
    """
    return max(projected_rates) - min(projected_rates)

def select_hedging_instrument(risk, insts):
    """
    This function based on evaluated risk will select the instrument that required to be hedged.
    Arguments:
        risk: This is the evaluated risk and it is floating.
        inst: This indicates a list of instruments available for hedging and it is a list.
    Returns:
        list: Based on the evaluated risk it will indicat the list of the appropriate instruments for hedging and it is a list.
    """
    if risk > 0.05:
        return [inst for inst in insts if isinstance(inst, InterestRateSwap)]
    else:
        return [inst for inst in insts if isinstance(inst, InterestRateOption)]
