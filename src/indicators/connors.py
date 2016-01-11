'''
Created on Jan 16, 2015

@author: oly
'''
from indicators import ProxiedMetric, MultiMetricMetric, RSI, PercentChange, AverageMetric, HistoricMetric
from indicators import AdjustedClose

class Streak(ProxiedMetric):
    def __init__(self, metric=None):
        ProxiedMetric.__init__(self, metric)
        self.val = None
        self.lastData = None
        
    def ready(self):
        if self.val == None:
            return False
        return True

    def value(self):
        return self.val
    
    def handle(self, perioddata):
        ProxiedMetric.handle(self, perioddata)
        if self.metric.ready():
            data = self.metric.value()
            if self.lastData != None:
                delta = data - self.lastData
                if delta > 0:
                    if self.val == None or self.val < 0:
                        self.val = 1.0
                    else:
                        self.val = self.val + 1.0
                if delta < 0:
                    if self.val == None or self.val > 0:
                        self.val = -1.0
                    else:
                        self.val = self.val - 1.0
                if delta == 0:
                    self.val = 0
            self.lastData = data
    
    def recommendedPreload(self):
        return ProxiedMetric.recommendedPreload(self) + 1

# returns 0-100 to represent percentile, not fractional, i.e. 50=50%
class PercentRank(ProxiedMetric):
    def __init__(self, period, metric=None):
        ProxiedMetric.__init__(self, metric)
        self.period = period
        self.lastData = None
        self.percentChange = PercentChange(metric)
        self._addMetric(self.percentChange)
        self.changes = list()
        self.val = None

    def ready(self):
        if self.val == None:
            return False
        else:
            return True
    
    def value(self):
        return self.val
    
    def handle(self, perioddata):
        ProxiedMetric.handle(self, perioddata)
        if self.percentChange.ready():
            nextchg = self.percentChange.value()
            if len (self.changes) == self.period:
                # have enough to calculate value, do it now before storing our latest value
                count = 0.0
                for pc in self.changes:
                    if pc < nextchg:
                        count = count+1.0
                self.val = 100*(count/float(self.period))
            self.changes.append(nextchg)
        if len(self.changes) > self.period:
            self.changes = self.changes[len(self.changes)-self.period:]
        pass
    
    def recommendedPreload(self):
        return ProxiedMetric.recommendedPreload(self) + self.period

class ConnorsRSI(MultiMetricMetric):
    def __init__(self, rsiPeriod, streakrsiPeriod, percentRankPeriod):
        MultiMetricMetric.__init__(self)
        self.close = AdjustedClose()
        self.rsi = RSI(metric=self.close,period=rsiPeriod)
        self.streak = Streak(metric=self.close)
        self.streakrsi = RSI(period=streakrsiPeriod, metric=self.streak)
        self.percentRank = PercentRank(metric=self.close, period=percentRankPeriod)
        self.average = AverageMetric(self.rsi, self.streakrsi, self.percentRank)
        self._addMetric(self.close)
        self._addMetric(self.rsi)
        self._addMetric(self.streak)
        self._addMetric(self.streakrsi)
        self._addMetric(self.percentRank)
        self._addMetric(self.average)
    
    def ready(self):
        return MultiMetricMetric.ready(self)
    
    def value(self):
        retval = self.average.value()
        return retval
    
    def handle(self, perioddata):
        MultiMetricMetric.handle(self, perioddata)

class CumulativeRSI(MultiMetricMetric):
    def __init__(self, period, rsiPeriod):
        MultiMetricMetric.__init__(self)
        self.rsis = list()
        rsi = RSI(rsiPeriod)
        self.rsis.append(rsi)
        self._addMetric(rsi)
        for i in range(1,period):
            hist = HistoricMetric(metric=rsi, period=i)
            self._addMetric(hist)
            self.rsis.append(hist)
    
    def ready(self):
        return MultiMetricMetric.ready(self)
    
    def value(self):
        retval = 0.0
        for rsi in self.rsis:
            if rsi.ready() == False:
                return None
            retval += rsi.value()
        return retval
    
    def handle(self, perioddata):
        MultiMetricMetric.handle(self, perioddata)
