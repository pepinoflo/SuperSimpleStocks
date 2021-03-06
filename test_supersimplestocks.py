''' Unit tests for module supersimplestocks.py. '''
import sys
import unittest
import datetime
import decimal
if sys.version_info < (3, 3):
    import mock
else:
    from unittest import mock
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

    def test_pe_ratio_returns_zero_when_dividend_is_zero(self):
        self.assertEqual(decimal.Decimal(0), self.tea.pe_ratio(12).quantize(SIXPLACES))

    def test_pe_ratio_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0).quantize(SIXPLACES), self.tea.pe_ratio(16).quantize(SIXPLACES))
        self.assertEqual(decimal.Decimal('32').quantize(SIXPLACES), self.pop.pe_ratio(16).quantize(SIXPLACES))

    ### Tests for volume_weighted_price method ###
    def test_volume_weighted_price_returns_zero_if_no_trades(self):
        self.assertEqual(0, self.tea.volume_weighted_price().quantize(SIXPLACES))

    def test_volume_weighted_price_returns_expected_value(self):
        # Here we patch datetime.now method in supersimplestocks module to input a fixed time instead
        with mock.patch('supersimplestocks.datetime') as mock_date:
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
        
class TestAllShareIndexMethod(unittest.TestCase):
    ''' Unit tests for all_share_index method. '''
    def setUp(self):
        # Here we create four mock objects for stock in order to mock the volume_weighted_price method. We use the class Stock as the spec to create the mock.
        self.stock1 = mock.create_autospec(supersimplestocks.Stock, spec_set=True, instance=True)
        self.stock2 = mock.create_autospec(supersimplestocks.Stock, spec_set=True, instance=True)
        self.stock3 = mock.create_autospec(supersimplestocks.Stock, spec_set=True, instance=True)
        self.stock4 = mock.create_autospec(supersimplestocks.Stock, spec_set=True, instance=True)
        self.stock1.volume_weighted_price.return_value = decimal.Decimal(24.16)
        self.stock2.volume_weighted_price.return_value = decimal.Decimal(2.91)
        self.stock3.volume_weighted_price.return_value = decimal.Decimal(0.24)
        self.stock4.volume_weighted_price.return_value = decimal.Decimal(0)

    def test_all_shares_index_returns_zero_when_empty_list_given(self):
        self.assertEqual(decimal.Decimal(0), supersimplestocks.all_shares_index([]))

    def test_all_shares_index_returns_zero_when_no_registered_trades(self):
        self.assertEqual(decimal.Decimal(0), supersimplestocks.all_shares_index([self.stock4]))

    def test_all_shares_index_returns_expected_value(self):
        stocks = [self.stock1, self.stock2 ,self.stock3, self.stock4]
        self.assertEqual(decimal.Decimal(2.56488).quantize(SIXPLACES), supersimplestocks.all_shares_index(stocks).quantize(SIXPLACES))


if __name__ == '__main__':
    decimal.getcontext().prec = 7
    unittest.main()

