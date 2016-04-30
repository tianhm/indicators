
from indicators.ehlers import TOSFisher
from stocklib.perioddata import PeriodData

import unittest

class EhlersTest(unittest.TestCase):
    def _fakePeriodOHLCData(self, open, high, low, close):
        return PeriodData(stock="SPY", date=None, open=open, high=high, low=low, close=close, adjustedClose=close, volume=1000000, period=60*60*24)

    def testFisher(self):
        fish = TOSFisher(period=10)
        # high,low,close - open does not matter
        for bar in [
            (190.2,187.16,189.11),
            (193.88,189.88,193.72),
            (194.58,191.84,193.65),
            (191.97,189.54,190.16),
            (191.78,187.1,191.3),
            (192.75,189.96,191.6),
            (191.67,187.2,187.95),
            (186.12,182.8,185.42),
            (186.94,183.2,185.43),
            (188.34,185.12,185.27),
            (184.1,181.09,182.86),
            (186.65,183.96,186.63),
            (189.81,187.63,189.78),
            (193.32,191.01,192.88),
            (193.27,191.72,192.09),
            (192.18,190.45,192),
            (194.95,193.79,194.78),
            (194.32,192.18,192.32),
            (193.53,189.32,193.2),
            (195.55,192.83,195.54),
            (196.68,194.9,195.09)]:
            fish.handle(self._fakePeriodOHLCData(bar[2],bar[0],bar[1],bar[2]))
        self.assertTrue(fish.ready())
        self.assertLess(abs(fish.value() - 2.09678), .05)

if __name__ == "__main__":
    unittest.main()