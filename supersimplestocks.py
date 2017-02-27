import decimal
import datetime

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
        try:
            return decimal.Decimal(market_price) / self.dividend_yield(market_price)
        except ZeroDivisionError as e:
            return 0

    def record_trade(self, trade):
        self.trades.append(trade)

    def volume_weighted_price(self):
        now = datetime.datetime.now()
        delta_fifteen_mins = datetime.timedelta(0, 15 * 60)
        total_trade_price = decimal.Decimal(0)
        total_shares = decimal.Decimal(0)
        for trade in self.trades:
            if now - trade.timestamp <= delta_fifteen_mins:
                total_trade_price += trade.price * trade.num_shares
                total_shares += trade.num_shares
        if total_shares == 0:
            return 0
        else:
            return total_trade_price / total_shares

class PreferredStock(Stock):
    ''' This class represents a preferred stock. '''
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend):
        super(PreferredStock, self).__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = decimal.Decimal(fixed_dividend)

    def dividend_yield(self, market_price):
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        return (self.fixed_dividend * self.par_value) / decimal.Decimal(market_price)

class Trade(object):
    def __init__(self, timestamp, num_shares, indicator, price):
        self.timestamp = timestamp
        self.num_shares = num_shares
        self.price = decimal.Decimal(price)
        if indicator == 'SELL' or indicator == 'BUY':
            self.indicator = indicator
        else:
            raise ValueError("Found: {}. Expected indicator should be SELL or BUY.".format(indicator))
