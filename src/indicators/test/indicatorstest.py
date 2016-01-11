'''
Created on Jan 13, 2015

@author: oly
'''
import unittest
from indicators.indicators import RSI
from stocklib.perioddata import PeriodData


class IndicatorsTest(unittest.TestCase):
    def _fakePeriodData(self, close):
        return PeriodData(stock="SPY", date=None, open=close, high=close, low=close, close=close, adjustedClose=close, volume=1000000, period=60*60*24)

    def testRSI(self):
        rsi = RSI(14)
        for close in [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46, 46.03, 46.41, 46.22]:
            rsi.handle(self._fakePeriodData(close))
        self.assertTrue(rsi.ready())
        self.assertTrue(rsi.value() < 67 and rsi.value() > 65)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRSI']
    unittest.main()