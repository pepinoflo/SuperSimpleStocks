''' Unit tests for module supersimplestocks.py. '''

import unittest
import unittest.mock
import datetime
import decimal
import supersimplestocks

SIXPLACES = decimal.Decimal('1.00000')

class TestStock(unittest.TestCase):
    ''' Unit tests for Stock class. '''

    def setUp(self):
        self.tea = supersimplestocks.Stock('TEA', 0, 100)
        self.pop = supersimplestocks.Stock('pop', 8, 100)
        self.ale = supersimplestocks.Stock('ale', 23, 100)
        self.joe = supersimplestocks.Stock('joe', 13, 100)

    ### Tests for dividend_yield method ###
    def test_dividend_yield_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, 0)

    def test_dividend_yield_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, -2)

    def test_dividend_yield_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0).quantize(SIXPLACES), self.tea.dividend_yield(16).quantize(SIXPLACES))
        self.assertEqual(decimal.Decimal(0.5).quantize(SIXPLACES), self.pop.dividend_yield(16).quantize(SIXPLACES))

    ### Tests for pe_ratio method ###
    def test_pe_ratio_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.tea.pe_ratio, 0)

    def test_pe_ratio_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.tea.pe_ratio, -2)

    def test_pe_ratio_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0).quantize(SIXPLACES), self.tea.pe_ratio(16).quantize(SIXPLACES))
        self.assertEqual(decimal.Decimal('32').quantize(SIXPLACES), self.pop.pe_ratio(16).quantize(SIXPLACES))

    ### Tests for pe_ratio method ###
    def test_volume_weighted_price_returns_zero_if_no_trades(self):
        self.assertEqual(0, self.tea.volume_weighted_price().quantize(SIXPLACES))

    def test_volume_weighted_price_returns_expected_value(self):
        # Here we patch datetime.now method in supersimplestocks module to input a fixed time instead
        with unittest.mock.patch('supersimplestocks.datetime') as mock_date:
            mock_date.datetime.now.return_value = datetime.datetime(2017, 2, 26, 16, 30, 5, 392218)
            mock_date.timedelta.side_effect = lambda *args, **kw: datetime.timedelta(*args, **kw)

            # We create 4 trades, trade 1 being outside of the last 15 minutes
            trade1 = supersimplestocks.Trade(datetime.datetime(2017, 2, 26, 16, 14, 2, 392218), 4, 'BUY', 23.55)
            trade2 = supersimplestocks.Trade(datetime.datetime(2017, 2, 26, 16, 15, 5, 392218), 3, 'BUY', 18.10)
            trade3 = supersimplestocks.Trade(datetime.datetime(2017, 2, 26, 16, 24, 5, 392217), 5, 'SELL', 3)
            trade4 = supersimplestocks.Trade(datetime.datetime(2017, 2, 26, 16, 30, 5, 392218), 18, 'BUY', 1.35)
            self.tea.record_trade(trade1)
            self.tea.record_trade(trade2)
            self.tea.record_trade(trade3)
            self.tea.record_trade(trade4)

            self.assertEqual(decimal.Decimal(3.6).quantize(SIXPLACES), self.tea.volume_weighted_price().quantize(SIXPLACES))

class TestPreferredStock(unittest.TestCase):
    ''' Unit tests for PreferredStock class. '''

    def setUp(self):
        self.gin = supersimplestocks.PreferredStock('gin', 8, 100, 0.02)
        
    def test_dividend_yield_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.gin.dividend_yield, 0)

    def test_dividend_yield_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.gin.dividend_yield, -2)

    def test_dividend_yield_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0.125).quantize(SIXPLACES), self.gin.dividend_yield(16).quantize(SIXPLACES))

class TestTrade(unittest.TestCase):
    ''' Unit tests for Trade class. '''
    def test_init_raises_ValueError_when_indicator_not_valid(self):
        self.assertRaises(ValueError, supersimplestocks.Trade, datetime.datetime(2017, 2, 26, 16, 33, 2, 392218), 4, 'GIVE', 47.37)

if __name__ == '__main__':
    decimal.getcontext().prec = 7
    unittest.main()

