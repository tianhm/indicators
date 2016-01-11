'''
Created on Jan 13, 2015

@author: oly
'''
import unittest
from stocklib.perioddata import PeriodData
from indicators.connors import ConnorsRSI, Streak, PercentRank
from indicators.indicators import AdjustedClose, RSI, AverageMetric,\
    PercentChange


class ConnorsTest(unittest.TestCase):
    def _fakePeriodData(self, close):
        return PeriodData(stock="SPY", date=None, open=close, high=close, low=close, close=close, adjustedClose=close, volume=1000000, period=60*60*24)

    def testStreak(self):
        # taken from Connors published example of Streak
        streak = Streak()
        streak.handle(self._fakePeriodData(20))
        streak.handle(self._fakePeriodData(20.5))
        self.assertTrue(streak.value() == 1)
        streak.handle(self._fakePeriodData(20.75))
        self.assertTrue(streak.value() == 2)
        streak.handle(self._fakePeriodData(19.75))
        self.assertTrue(streak.value() == -1)
        streak.handle(self._fakePeriodData(19.50))
        self.assertTrue(streak.value() == -2)
        streak.handle(self._fakePeriodData(19.35))
        self.assertTrue(streak.value() == -3)
        streak.handle(self._fakePeriodData(19.35))
        self.assertTrue(streak.value() == 0)
        streak.handle(self._fakePeriodData(19.4))
        self.assertTrue(streak.value() == 1)
    
    def testPercentRank(self):
        pr = PercentRank(period=5)
        pr.handle(self._fakePeriodData(10))
        pr.handle(self._fakePeriodData(9.9))
        pr.handle(self._fakePeriodData(9.85))
        pr.handle(self._fakePeriodData(9.9))
        pr.handle(self._fakePeriodData(10))
        pr.handle(self._fakePeriodData(10.1))
        pr.handle(self._fakePeriodData(10.10001))
        self.assertTrue(pr.value() == 40)
        pr.handle(self._fakePeriodData(10))
        pr.handle(self._fakePeriodData(10.1))
        pr.handle(self._fakePeriodData(10.3))
        pr.handle(self._fakePeriodData(11))
        pr.handle(self._fakePeriodData(13))
        pr.handle(self._fakePeriodData(12.5))
        pr.handle(self._fakePeriodData(1))
        self.assertTrue(pr.value() == 0)
        pr.handle(self._fakePeriodData(10))
        pr.handle(self._fakePeriodData(9.9))
        pr.handle(self._fakePeriodData(9.3))
        pr.handle(self._fakePeriodData(9))
        pr.handle(self._fakePeriodData(8))
        pr.handle(self._fakePeriodData(8.1))
        pr.handle(self._fakePeriodData(209))
        self.assertTrue(pr.value() == 100)
    
    def testPercentChange(self):
        pc = PercentChange()
        pc.handle(self._fakePeriodData(10.0))
        pc.handle(self._fakePeriodData(9.0))
        self.assertTrue(pc.value() == -0.1)
        pc.handle(self._fakePeriodData(9.45))
        self.assertTrue(pc.value() >= 0.049 and pc.value() <= 0.051)
        
    def testConnorsRSI(self):

        crsi = ConnorsRSI(3,2,100)
        
        # to figure out what the fuck is wrong
#         aclose = AdjustedClose()
#         rsi = RSI(metric=aclose,period=3)
#         streak = Streak(metric=aclose)
#         streakrsi = RSI(period=2, metric=streak)
#         percentRank = PercentRank(metric=aclose, period=100)
#         average = AverageMetric(rsi, streakrsi, percentRank)

        closes = [25.38,25.74,26.7,25.61,24.83,25.01,25.68,25.7,26.69, \
                  26.5,26.02,26.39,26.01,25.64,26.51,26.29,27.04,26.96,26.43,26.99,26,25.73,25.63,25.56,26.3,25.68, \
                  25.08,24.96,25.14,25.21,24.19,23.89,24.64,23.64,23.71,24.62,24.13,23.44,23.6,24.45,23.82,24.73, \
                  24.26,24.9,25.04,25.46,25.66,25.18,25.62,25.02,24.85,24.88,25.08,23.4,22.68,20.77,20.97,19.11, \
                  19.57,17.9,18.88,18.88,19.73,19.19,19.63,18.09,17.26,17.34,17.81,17.29,16.93,17.31,17.72,17.9, \
                  18.86,18.58,17.17,16.79,17.46,17.16,15.63,15.63,15.59,15.74,15.97,15.57,15.16,14.35,13.38,11.58, \
                  11.11,11.3,12.06,11.01,10.84,10.19,9.22,9.28,9.63,10.61,9.99,11.14,10.67,11.4,11.59,11.89,11.1, \
                  11.64,11.05,11.24,11.73,13.02,12.37,12.87,13.85,14.4,13.14,12.06,12.62,12.94,12.96,13.44,13.64, \
                  11.87,11.99,12.55,12.57,11.93,11.35,10.21,10.23,9.42,9.64,9.1,8.97,9.43,9.68,10.89,10.99,11.12, \
                  11.74,10.45,10.22,9.71,10.02,9.3,9.09,9,8.68,8.95,8.18,8.55,8.35,8.4,8.37,8.19,7.9,8.36,8.5,9.07, \
                  9.23,9.19,9.05,9.16,9.56,9.68,10.05,9.51,9.81,10.3,10.53,10.42,10.99,10.86,11.47,10.93,11.1,10.95, \
                  11.09,11.39,11.13,12.37,12.07,11.74,11.54,11.46,10.68,11.21,10.9,10.48,10.79,10.66,10.7,10.75,10.67, \
                  11.42,11.3,11.46,11.1,11.32,11.19,10.56,9.7,10.14,10.2,10.3,10.14,10.23,10.42,10.71,10.88,10.81,10.47, \
                  10.43,9.83,9.81,9.94,9.7,9.38,9.1,8.98,9.51,9.39,9.06,8.96,8.88,8.64,8.83,9.41,9.48,9.14,8.93,8.74,8.6, \
                  8.65,8.45,8.66,8.8,8.92,8.72,8.69,8.63,8.24,7.75,7.44,7.49,7.21,7.14,7.26,7.22,6.79,6.43, 6.42, 5.91,]

#         mincrsi = None
#         maxcrsi = None
#         minrsi = None
#         maxrsi = None
#         minstreak = None
#         maxstreak = None
#         minstreakrsi = None
#         maxstreakrsi = None
#         minpercentrank = None
#         maxpercentrank = None

        for close in closes:
            pd = self._fakePeriodData(close)
            crsi.handle(pd)
#             aclose.handle(pd)
#             rsi.handle(pd)
#             streak.handle(pd)
#             streakrsi.handle(pd)
#             percentRank.handle(pd)
#             average.handle(pd)
            
#             if crsi.ready() and (mincrsi == None or mincrsi > crsi.value()):
#                 mincrsi = crsi.value()
#             if crsi.ready() and (maxcrsi == None or maxcrsi < crsi.value()):
#                 maxcrsi = crsi.value()
#             if rsi.ready() and (minrsi == None or minrsi > rsi.value()):
#                 minrsi = rsi.value()
#             if rsi.ready() and (maxrsi == None or maxrsi < rsi.value()):
#                 maxrsi = rsi.value()
#             if streak.ready() and (minstreak == None or minstreak > streak.value()):
#                 minstreak = streak.value()
#             if streak.ready() and (maxstreak == None or maxstreak < streak.value()):
#                 maxstreak = streak.value()
#             if streakrsi.ready() and (minstreakrsi == None or minstreakrsi > streakrsi.value()):
#                 minstreakrsi = streakrsi.value()
#             if streakrsi.ready() and (maxstreakrsi == None or maxstreakrsi < streakrsi.value()):
#                 maxstreakrsi = streakrsi.value()
#             if percentRank.ready() and (minpercentrank == None or minpercentrank > percentRank.value()):
#                 minpercentrank = percentRank.value()
#             if percentRank.ready() and (maxpercentrank == None or maxpercentrank < percentRank.value()):
#                 maxpercentrank = percentRank.value()
        
        
        self.assertTrue(crsi.ready())
#         print "CRSI: %f - %f" % (mincrsi, maxcrsi)
#         print "RSI: %f - %f" % (minrsi, maxrsi)
#         print "Streak: %f - %f" % (minstreak, maxstreak)
#         print "Streak RSI: %f - %f" % (minstreakrsi, maxstreakrsi)
#         print "Percent Rank: %f - %f" % (minpercentrank, maxpercentrank)
#         print rsi.value()
        print crsi.value()
        self.assertTrue(crsi.value() < 2.38 and crsi.value() > 2.37)

if __name__ == "__main__":
#     ct = ConnorsTest()
#     ct.testConnorsRSI()
    unittest.main()
    
    
    minrsi = None
    maxrsi = None
    minstreak = None
    maxstreak = None
    minstreakrsi = None
    maxstreakrsi = None
    minpercentrank = None
    maxpercentrank = None
    minaverage = None
    maxaverage = None
    
    
#             aclose.handle(pd)
#             rsi.handle(pd)
#             streak.handle(pd)
#             streakrsi.handle(pd)
#             percentRank.handle(pd)
#             average.handle(pd)
