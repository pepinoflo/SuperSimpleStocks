class Stock(object):
    ''' This class represents a common stock. '''

    def __init__(self, symbol, last_dividend, par_value):
        self.symbol = symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.trades = []

class PreferredStock(Stock):
    ''' This class represents a preferred stock. '''
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend):
        super(PreferredStock, self).__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = fixed_dividend
