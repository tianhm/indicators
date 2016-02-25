"""
Created on Apr 16, 2015

@author: oly@barefootanalytics.com
"""
from indicators import MultiMetricMetric
from indicators import Low, High, Lowest, Highest
from indicators import Divide, Subtract, Multiply,\
    SimpleMovingAverage, Value
from indicators import Close
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Stochastics(MultiMetricMetric):
    """ Implementation of Full Stochastsics

    For Slow Stochastics, pass a kperiod of 3.  For Fast Stochastics,
    pass a kperiod of 1.  In other words, if you want Fast Stochastics(14,3)
    in terms of a trading chart, use Stochastics(14,1,3) here.
    """
    def __init__(self, period, kperiod, dperiod):
        MultiMetricMetric.__init__(self)
        self.period = period
        self.dperiod = dperiod
        self.close = Close()
        self.low = Low()
        self.high = High()
        self.lowest = Lowest(self.low,self.period)
        self.highest = Highest(self.high, self.period)
        self.closediff = Subtract(self.close, self.lowest)
        self.highdiff = Subtract(self.highest, self.lowest)
        self.percentKRaw = Divide(self.closediff, self.highdiff)
        self.pK = Multiply(self.percentKRaw, Value(100.0))
        self.slowK = SimpleMovingAverage(metric=self.pK, period=kperiod)
        self.pD = SimpleMovingAverage(metric=self.slowK, period=self.dperiod)

        self._addMetrics(self.close, self.low, self.high, self.lowest,
                         self.highest, self.closediff, self.highdiff,
                         self.percentKRaw, self.pK, self.slowK, self.pD)

    def value(self):
        return self.pD.value()

    def percentK(self):
        return self.pK.value()

    def slowK(self):
        return self.slowK.value()