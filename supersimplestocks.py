import decimal
import datetime

class Stock(object):
    ''' This class represents a common stock. '''

    def __init__(self, symbol, last_dividend, par_value):
        '''
        :param str symbol: The symbol defining the stock
        :param float last_dividend: The last dividend
        :param int par_value: The par value
        '''
        self.symbol = symbol
        self.last_dividend = decimal.Decimal(last_dividend)
        self.par_value = decimal.Decimal(par_value)
        self.trades = []

    def dividend_yield(self, market_price):
        '''
        Calculates the dividend yield

        :param float market_price: The market price
        :return: the dividend yield
        :rtype: Decimal
        :raises ValueError: If the market price is negative or zero.
        '''
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        return self.last_dividend / decimal.Decimal(market_price)

    def pe_ratio(self, market_price):
        '''
        Calculates the simplified Price-Earnings ratio. The dividend yield is used in the formula. If the dividend yield is zero, it returns zero.

        :param float market_price: The market price
        :return: the Price-Earnings ratio
        :rtype: Decimal
        :raises ValueError: If the market price is negative or zero.
        '''
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        try:
            return decimal.Decimal(market_price) / self.dividend_yield(market_price)
        except ZeroDivisionError as e:
            return decimal.Decimal(0)

    def record_trade(self, trade):
        '''
        Records a trade for this stock.

        :param Trade trade: The trade
        '''
        self.trades.append(trade)

    def volume_weighted_price(self):
        '''
        Calculates the Volume Weighted Price for all the trades in the last 15 minutes. If this stock does not have any trade, the method returns zero.

        :return: The Volume Weighted Price
        :rtype: Decimal
        '''
        now = datetime.datetime.now()
        delta_fifteen_mins = datetime.timedelta(0, 15 * 60)
        total_trade_price = decimal.Decimal(0)
        total_shares = decimal.Decimal(0)
        for trade in self.trades:
            if now - trade.timestamp <= delta_fifteen_mins:
                total_trade_price += trade.price * trade.num_shares
                total_shares += trade.num_shares
        if total_shares == 0:
            return decimal.Decimal(0)
        else:
            return total_trade_price / total_shares

class PreferredStock(Stock):
    ''' This class represents a preferred stock. '''
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend):
        '''
        :param str symbol: The symbol defining the stock
        :param float last_dividend: The last dividend
        :param int par_value: The par value
        :param float fixed_dividend: The fixed dividend
        '''
        super(PreferredStock, self).__init__(symbol, last_dividend, par_value)
        self.fixed_dividend = decimal.Decimal(fixed_dividend)

    def dividend_yield(self, market_price):
        '''
        Calculates the dividend yield

        :param float market_price: The market price
        :return: the dividend yield
        :rtype: Decimal
        :raises ValueError: If the market price is negative or zero.
        '''
        if market_price <= 0:
            raise ValueError("market price value is negative or equal to 0. Found {}".format(market_price))
        return (self.fixed_dividend * self.par_value) / decimal.Decimal(market_price)

class Trade(object):
    ''' This class represents a Trade. '''
    def __init__(self, timestamp, num_shares, indicator, price):
        '''
        :param datetime timestamp: A timestamp of when the trade has been completed
        :param int num_shares: The number of shares bought or sold
        :param str indicator: SELL or BUY indicator
        :param float price: The price
        :raises ValueError: If the indicator is neither BUY or SELL
        '''
        self.timestamp = timestamp
        self.num_shares = num_shares
        self.price = decimal.Decimal(price)
        if indicator == 'SELL' or indicator == 'BUY':
            self.indicator = indicator
        else:
            raise ValueError("Found: {}. Expected indicator should be SELL or BUY.".format(indicator))

def all_shares_index(stocks):
    '''
    Calculates the All Shares Index for a given list of stocks. If the list is empty, it will return 0. If there is one stock whose price is 0, this stock is not taken into account in the calculation.

    :param list stocks: The list of stocks
    :return: The all shares index
    :rtype: Decimal
    '''
    if not stocks:
        return decimal.Decimal(0)
    mult_stocks_price = decimal.Decimal(1)
    num_stocks = 0
    for stock in stocks:
        vwp = stock.volume_weighted_price()
        if vwp != 0:
            mult_stocks_price *= vwp
            num_stocks += 1
    if num_stocks == 0:
        return decimal.Decimal(0)
    # We use 1.0 in the power to support Python 2 and 3
    return mult_stocks_price ** decimal.Decimal((1.0/num_stocks))


if __name__ == '__main__':
    decimal.getcontext().prec = 6
    stocks = {'TEA': Stock('TEA', 0, 100),
              'POP': Stock('POP', 8, 100),
              'ALE': Stock('ALE', 23, 60),
              'GIN': PreferredStock('GIN', 8, 0.02, 100),
              'JOE': Stock('JOE', 13, 250)
             }
    now = datetime.datetime.now()
    stocks['TEA'].record_trade(Trade(now, 6, 'BUY', 24.12))
    stocks['TEA'].record_trade(Trade(now, 4, 'BUY', 98.45))
    stocks['POP'].record_trade(Trade(now, 12, 'SELL', 112.01))
    stocks['POP'].record_trade(Trade(now, 2, 'BUY', 45))
    stocks['POP'].record_trade(Trade(now, 32, 'SELL', 23.23))
    stocks['ALE'].record_trade(Trade(now, 1, 'SELL', 134.20))
    stocks['ALE'].record_trade(Trade(now, 18, 'SELL', 32.14))
    stocks['GIN'].record_trade(Trade(now, 7, 'BUY', 86.31))
    stocks['GIN'].record_trade(Trade(now, 22, 'SELL', 234))

    print('========================================================')
    print('  Stock     dividend yield     pe ratio     vwp  ')
    print('   TEA        {}             {}            {}   '.format(stocks['TEA'].dividend_yield(35.21), stocks['TEA'].pe_ratio(35.21), stocks['TEA'].volume_weighted_price()))
    print('   POP        {}          {}      {}   '.format(stocks['POP'].dividend_yield(12.30), stocks['POP'].pe_ratio(12.30), stocks['POP'].volume_weighted_price()))
    print('   ALE        {}          {}      {}   '.format(stocks['ALE'].dividend_yield(137.93), stocks['ALE'].pe_ratio(137.93), stocks['ALE'].volume_weighted_price()))
    print('   GIN        {}         {}      {}   '.format(stocks['GIN'].dividend_yield(85), stocks['GIN'].pe_ratio(85), stocks['GIN'].volume_weighted_price()))
    print('   JOE        {}           {}    {}   '.format(stocks['JOE'].dividend_yield(1.01), stocks['JOE'].pe_ratio(1.01), stocks['JOE'].volume_weighted_price()))
    print()
    print('GBCE all shares index: {}'.format(all_shares_index(stocks.values())))
    print('========================================================')
