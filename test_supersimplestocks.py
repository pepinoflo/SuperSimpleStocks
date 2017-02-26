''' Unit tests for module supersimplestocks.py. '''

import unittest
import decimal
from supersimplestocks import *

class TestStocks(unittest.TestCase):
    ''' Unit tests for supersimplestocks module. '''

    def setUp(self):
        self.tea = Stock('TEA', 0, 100)
        self.pop = Stock('pop', 8, 100)
        self.ale = Stock('ale', 23, 100)
        self.gin = PreferredStock('gin', 8, 100, 0.02)
        self.joe = Stock('joe', 13, 100)
        
    def test_dividend_yield_raise_ValueError_when_market_price_is_zero(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, 0)

    def test_dividend_yield_raise_ValueError_when_market_price_is_negative(self):
        self.assertRaises(ValueError, self.tea.dividend_yield, -2)

    def test_dividend_yield_returns_expected_decimal(self):
        self.assertEqual(decimal.Decimal(0), self.tea.dividend_yield(16))
        self.assertEqual(decimal.Decimal(0.5), self.pop.dividend_yield(16))

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

if __name__ == '__main__':
    decimal.getcontext().prec = 8
    unittest.main()

