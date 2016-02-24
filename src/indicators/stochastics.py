'''
Created on Apr 16, 2015

@author: oly
'''
from indicators import MultiMetricMetric
from indicators import Low, High, Lowest, Highest
from indicators import Divide, Subtract, Multiply,\
    SimpleMovingAverage, Value
from indicators import Close
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Stochastics(MultiMetricMetric):
    def __init__(self, period, dperiod):
        log.warn("Stochastics are in progress and values may be wrong")
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
        self.pD = SimpleMovingAverage(metric=self.pK, period=self.dperiod)
        self._addMetrics(self.close, self.low, self.high, self.lowest, \
                         self.highest, self.closediff, self.highdiff, \
                         self.percentKRaw, self.pK, self.pD)

    def value(self):
        return self.pD.value()

    def percentK(self):
        return self.pK.value()
