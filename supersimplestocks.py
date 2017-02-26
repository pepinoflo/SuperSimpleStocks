import decimal

class Stock(object):
    ''' This class represents a common stock. '''

    def __init__(self, symbol, last_dividend, par_value):
        self.symbol = symbol
        self.last_dividend = decimal.Decimal(last_dividend)
        self.par_value = decimal.Decimal(par_value)
        self.trades = []

    def dividend_yield(self, market_price):
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        return self.last_dividend / decimal.Decimal(market_price)

    def pe_ratio(self, market_price):
        pass

class PreferredStock(Stock):
    ''' This class represents a preferred stock. '''
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend):
        super(PreferredStock, self).__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = decimal.Decimal(fixed_dividend)

    def dividend_yield(self, market_price):
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        return (self.fixed_dividend * self.par_value) / decimal.Decimal(market_price)
