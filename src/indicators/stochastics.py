'''
Created on Apr 16, 2015

@author: oly
'''
from indicators import Metric
from indicators import Low, High, Lowest, Highest
from indicators import Divide, Subtract, Multiply,\
    SimpleMovingAverage, Value
from indicators import Close

class Stochastics(Metric):
    def __init__(self, period, dperiod):
        Metric.__init__(self)
        self.period = period
        self.dperiod = dperiod
        self.percentK = None
        self.percentD = None
        self.close = Close()
        self.low = Low()
        self.high = High()
        self.lowest = Lowest(self.low,self.period)
        self.highest = Highest(self.high, self.period)
        self.closediff = Subtract(self.close, self.lowest)
        self.highdiff = Subtract(self.highest, self.lowest)
        self.percentKRaw = Divide(self.closediff, self.highdiff)
        self.percentK = Multiply(self.percentKRaw, Value(100.0))
        self.percentD = SimpleMovingAverage(self.percentK, self.dperiod)

    def handle(self, perioddata):
        Metric.handle(self, perioddata)
        self.close.handle(perioddata)
        self.low.handle(perioddata)
        self.high.handle(perioddata)
        self.lowest.handle(perioddata)
        self.highest.handle(perioddata)
        self.closediff.handle(perioddata)
        self.highdiff.handle(perioddata)
        self.percentKRaw.handle(perioddata)
        self.percentK.handle(perioddata)
        self.percentD.handle(perioddata)

    def ready(self):
        return self.percentD.ready()
    
    def value(self):
        return self.percentD.value()
    
    def recommendedPreload(self):
        return self.percentD.recommendedPreload()