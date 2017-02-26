''' Unit tests for module supersimplestocks.py. '''

import unittest
import datetime
import decimal
from supersimplestocks import *

class TestStock(unittest.TestCase):
    ''' Unit tests for Stock class. '''

    def setUp(self):
        self.tea = Stock('TEA', 0, 100)
        self.pop = Stock('pop', 8, 100)
        self.ale = Stock('ale', 23, 100)
        self.joe = Stock('joe', 13, 100)

    ### Tests for dividend_yield method ###
    def test_dividend_yield_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, 0)

    def test_dividend_yield_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, -2)

    def test_dividend_yield_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0), self.tea.dividend_yield(16))
        self.assertEqual(decimal.Decimal(0.5), self.pop.dividend_yield(16))

    ### Tests for pe_ratio method ###
    def test_pe_ratio_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.tea.pe_ratio, 0)

    def test_pe_ratio_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.tea.pe_ratio, -2)

    def test_pe_ratio_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0), self.tea.pe_ratio(16))
        self.assertEqual(decimal.Decimal(32), self.pop.pe_ratio(16))

class TestPreferredStock(unittest.TestCase):
    ''' Unit tests for PreferredStock class. '''

    def setUp(self):
        self.gin = PreferredStock('gin', 8, 100, 0.02)
        
    def test_dividend_yield_raises_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.gin.dividend_yield, 0)

    def test_dividend_yield_raises_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.gin.dividend_yield, -2)

    def test_dividend_yield_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0.125), self.gin.dividend_yield(16))

class TestTrade(unittest.TestCase):
    ''' Unit tests for Trade class. '''
    def test_init_raises_ValueError_when_indicator_not_valid(self):
        self.assertRaises(ValueError, Trade, datetime.datetime(2017, 2, 26, 16, 33, 2, 392218), 4, 'GIVE', 47.37)

if __name__ == '__main__':
    decimal.getcontext().prec = 8
    unittest.main()

