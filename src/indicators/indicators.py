'''
Created on Dec 14, 2014

@author: oly@oberdorf.org
'''

import numpy

from cmath import sqrt
from numpy import log, average
from __builtin__ import False

class Metric:
    def __init__(self):
        pass

    def value(self):
        return 0

    def ready(self):
        return False

    def handle(self, perioddata):
        pass

    def recommendedPreload(self):
        return 0

class Add(Metric):
    def __init__(self, metric1, metric2):
        self.metric1=metric1
        self.metric2=metric2

    def value(self):
        return self.metric1.value() + self.metric2.value()

    def ready(self):
        if self.metric1.ready() and self.metric2.ready():
            return True
        return False

    def handle(self, periodData):
        pass

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Subtract(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        return self.metric1.value() - self.metric2.value()

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Multiply(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        a = self.metric1.value()
        b = self.metric2.value()
        return a*b

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Divide(Metric):
    def __init__(self, metric1, metric2):
        self.metric1 = metric1
        self.metric2 = metric2

    def value(self):
        a = self.metric1.value()
        b = self.metric2.value()
        if a == 0:
            return 0
        if b == 0:
            return 0
        return a/b

    def ready(self):
        return self.metric1.ready() and self.metric2.ready()

    def recommendedPreload(self):
        return max(self.metric1.recommendedPreload(), self.metric2.recommendedPreload())

class Abs(Metric):
    def __init__(self, metric):
        self.metric = metric

    def value(self):
        if self.metric.ready():
            return abs(self.metric.value())
        return 0

    def ready(self):
        return self.metric.ready()

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class Max(Metric):
    def __init__(self, metrica, metricb):
        self.metrica = metrica
        self.metricb = metricb

    def value(self):
        if self.ready() == False:
            return None
        return max(self.metrica.value(), self.metricb.value())

    def ready(self):
        return self.metrica.ready() and self.metricb.ready()

    def recommendedPreload(self):
        return max(self.metrica.recommendedPreload(), self.metricb.recommendedPreload())

class Value(Metric):
    def __init__(self, value):
        self.val = value

    def value(self):
        return self.val

    def ready(self):
        return True

class Open(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, perioddata):
        self.val = perioddata.open

class Close(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.close

class AdjustedClose(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedClose != None:
            self.val = periodData.adjustedClose

class AdjustedOpen(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedOpen != None:
            self.val = periodData.adjustedOpen

class AdjustedHigh(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedHigh != None:
            self.val = periodData.adjustedHigh

class AdjustedLow(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if periodData != None and periodData.adjustedLow != None:
            self.val = periodData.adjustedLow

class High(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.high

class Low(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if periodData != None and periodData.close != None:
            self.val = periodData.low

class Volume(Metric):
    def __init__(self):
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, perioddata):
        self.val = perioddata.volume

class MultiMetricMetric(Metric):
    def __init__(self):
        self.metrics = list()

    def _addMetric(self, metric):
        self.metrics.append(metric)

    def ready(self):
        for metric in self.metrics:
            if metric.ready() == False:
                return False
        return True

    def handle(self, perioddata):
        for metric in self.metrics:
            metric.handle(perioddata)

    def recommendedPreload(self):
        retval = 0
        for metric in self.metrics:
            if metric.recommendedPreload() > retval:
                retval = metric.recommendedPreload()
        return retval

class AverageMetric(Metric):
    def __init__(self, *metrics):
        self.count=0
        self.metrics = metrics
        self.count = len(self.metrics)

    def ready(self):
        for metric in self.metrics:
            if not metric.ready():
                return False
        return True

    def value(self):
        values = list()
        for metric in self.metrics:
            if metric.ready() == False:
                return None
            values.append(metric.value())
        count = 0.0
        sum = 0.0
        for value in values:
            sum = sum + value
            count = count + 1.0
        if count == 0:
            return 0
        return sum/count
        #return average(values)

# had to be after Close definition
class ProxiedMetric(MultiMetricMetric):
    def __init__(self, metric):
        MultiMetricMetric.__init__(self)
        if metric == None:
            self.metric = Close()
            self._addMetric(self.metric)
        else:
            # do not manage it, just track it
            self.metric = metric

    def ready(self):
        return self.metric.ready()

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class PercentChange(ProxiedMetric):
    def __init__(self, metric=None):
        ProxiedMetric.__init__(self, metric)
        self.lastData = None
        self.val = None

    def ready(self):
        if self.val == None:
            return False
        return True

    def value(self):
        return self.val

    def handle(self, perioddata):
        ProxiedMetric.handle(self, perioddata)
        if self.metric.ready():
            if self.lastData != None:
                if self.lastData == 0:
                    self.val = 0
                else:
                    self.val = (self.metric.value() - self.lastData)/self.lastData
            self.lastData = self.metric.value()

    def recommendedPreload(self):
        return ProxiedMetric.recommendedPreload(self) + 1

class Highest(Metric):
    def __init__(self, metric, period):
        self.metric=metric
        self.period=period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return max(self.data)

    def ready(self):
        if len(self.data) == 0:
            return False
        if self.period == -1 and len(self.data)>0:
            return True
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if self.period > 0 and len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class Lowest(Metric):
    def __init__(self, metric, period):
        self.metric=metric
        self.period=period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return min(self.data)

    def ready(self):
        if len(self.data) == 0:
            return False
        if self.period == -1 and len(self.data)>0:
            return True
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if self.period > 0 and len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class SimpleMovingAverage(Metric):
    def __init__(self, metric=None, period=20):
        if metric == None:
            self.metric = AdjustedClose()
            self.manageMetric=True
        else:
            self.metric = metric
            self.manageMetric=False
        self.period = period
        self.data = list()

    def value(self):
        if len(self.data) < self.period:
            return None
        return numpy.average(self.data)

    def ready(self):
        if len(self.data) >= self.period:
            return True
        return False

    def handle(self, periodData):
        # TODO a carousel approach would be faster, where we continuously
        # update the index to drop and replace that element with the new
        # data point.  updating a list element is constant-time, while
        # removing the first element is slow for large lists.
        if self.manageMetric ==  True:
            self.metric.handle(periodData)
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data) > self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class ExponentialMovingAverage(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.multiplier = (2.0/(period+1))
        self.sma = SimpleMovingAverage(metric, period)
        self.period = period
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.sma != None:
            self.sma.handle(periodData)
            if self.sma.ready():
                self.val = self.sma.value()
                self.sma = None
        if self.val != None:
            newdat = self.metric.value()
            self.val = (newdat - self.val)*self.multiplier + self.val

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class TrueRange(Metric):
    def __init__(self):
        self.val = None
        self.lastClose = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.lastClose == None:
            self.lastClose = periodData.close
        self.val = max(periodData.high-periodData.low,self.lastClose-periodData.low,periodData.high-self.lastClose)
        self.lastClose = periodData.close

    def recommendedPreload(self):
        return 1


class AdjustedTrueRange(Metric):
    def __init__(self):
        self.val = None
        self.lastClose = None

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.lastClose == None:
            self.lastClose = periodData.adjustedClose
        self.val = max(periodData.adjustedHigh-periodData.adjustedLow,self.lastClose-periodData.adjustedLow,periodData.adjustedHigh-self.lastClose)
        self.lastClose = periodData.adjustedClose

    def recommendedPreload(self):
        return 1

class DMPos(Metric):
    def __init__(self):
        self.lasthigh = None
        self.lastlow = None
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if self.lasthigh != None and self.lastlow != None:
            up = max(periodData.high - self.lasthigh,0)
            down = max(self.lastlow - periodData.low, 0)
            if (up > down):
                self.val = up
            else:
                self.val = 0
        self.lasthigh = periodData.high
        self.lastlow = periodData.low

    def recommendedPreload(self):
        return 1

class DMNeg(Metric):
    def __init__(self):
        self.lasthigh = None
        self.lastlow = None
        self.val = None

    def value(self):
        return self.val

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self,periodData):
        if self.lasthigh != None and self.lastlow != None:
            up = max(periodData.high - self.lasthigh,0)
            down = max(self.lastlow - periodData.low, 0)
            if (up < down):
                self.val = down
            else:
                self.val = 0
        self.lasthigh = periodData.high
        self.lastlow = periodData.low

    def recommendedPreload(self):
        return 1

class _ADXSmoother(Metric):
    def __init__(self,metric,period):
        self.metric = metric
        self.period = period
        self.val = None
        self.aggregator = list()

    def value(self):
        return self.val / self.period

    def ready(self):
        if self.val == None:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.aggregator != None:
            self.aggregator.append(self.metric.value())
            if len(self.aggregator) == self.period:
                self.val = sum(self.aggregator)
                self.aggregator = None
        if self.val != None:
            self.val = self.val * (1.0-(1.0/self.period)) + self.metric.value()

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class ADR(Metric):
    def __init__(self,period):
        self.high = High()
        self.low = Low()
        self.dr = Subtract(self.high, self.low)
        self.drav = SimpleMovingAverage(self.dr,period)

    def value(self):
        if self.drav.ready():
            return self.drav.value()
        return None

    def ready(self):
        return self.drav.ready()

    def handle(self, periodData):
        self.high.handle(periodData)
        self.low.handle(periodData)
        self.dr.handle(periodData)
        self.drav.handle(periodData)

    def recommendedPreload(self):
        return self.drav.recommendedPreload()

class ATR(Metric):
    def __init__(self,period):
        self.tr = TrueRange()
        self.trav = _ADXSmoother(self.tr,period)

    def value(self):
        if self.trav.ready():
            return self.trav.value()
        return None

    def ready(self):
        return self.trav.ready()

    def handle(self, periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)

    def recommendedPreload(self):
        return self.trav.recommendedPreload()

class AdjustedATR(Metric):
    def __init__(self,period):
        self.tr = AdjustedTrueRange()
        self.trav = _ADXSmoother(self.tr,period)

    def value(self):
        if self.trav.ready():
            return self.trav.value()
        return None

    def ready(self):
        return self.trav.ready()

    def handle(self, periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)

    def recommendedPreload(self):
        return self.trav.recommendedPreload()

class HistoricMetric(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.period = period
        self.data = list()

    def value(self):
        if self.ready():
            return self.data[self.period]
        return None

    def ready(self):
        if len(self.data)>self.period:
            return True
        return False

    def handle(self,periodData):
        if self.metric.ready():
            self.data.insert(0, self.metric.value())
        if len(self.data) > (self.period+1):
            self.data = self.data[0:self.period+1]

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class _ADXAverager(Metric):
    def __init__(self,metric,period):
        self.aggregator = list()
        self.val = None
        self.period = period
        self.metric = metric

    def value(self):
        return self.val

    def ready(self):
        if self.val != None:
            return True
        return False

    def handle(self, periodData):
        if self.metric.ready() == False:
            return
        if self.aggregator != None:
            self.aggregator.append(self.metric.value())
            if len(self.aggregator) == self.period:
                self.val = sum(self.aggregator)/self.period
                self.aggregator = None
        if self.val != None:
            self.val = self.val * (1.0-(1.0/self.period)) + self.metric.value() * (1.0/self.period)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class ADX(Metric):
    def __init__(self,period):
        self.period = period
        self.tr = TrueRange()
        self.trav = _ADXSmoother(self.tr, period)
        self.dmpos = DMPos()
        self.dmneg = DMNeg()
        self.dmposav = _ADXSmoother(self.dmpos, period)
        self.dmnegav = _ADXSmoother(self.dmneg, period)
        self.dipos = Divide(self.dmposav, self.trav)
        self.dineg = Divide(self.dmnegav, self.trav)
        self.didiff = Subtract(self.dipos, self.dineg)
        self.didiffabs = Abs(self.didiff)
        self.disum = Add(self.dipos, self.dineg)
        self.dx = Divide(self.didiffabs, self.disum)
        self.adx = _ADXAverager(self.dx, period)

    def value(self):
        if self.adx.ready():
            return self.adx.value() * 100.0
        else:
            return 0.0

    def ready(self):
        return self.adx.ready()

    def handle(self,periodData):
        self.tr.handle(periodData)
        self.trav.handle(periodData)
        self.dmpos.handle(periodData)
        self.dmneg.handle(periodData)
        self.dmposav.handle(periodData)
        self.dmnegav.handle(periodData)
        self.dipos.handle(periodData)
        self.dineg.handle(periodData)
        self.didiff.handle(periodData)
        self.didiffabs.handle(periodData)
        self.disum.handle(periodData)
        self.dx.handle(periodData)
        self.adx.handle(periodData)

    def diPos(self):
        if self.ready():
            return self.dipos.value()
        return None

    def diNeg(self):
        if self.ready():
            return self.dineg.value()

    def recommendedPreload(self):
        return self.adx.recommendedPreload()

class BollingerBands(Metric):
    def __init__(self, period=20, stdev=2.0, metric=None):
        if metric == None:
            self.metric       = Close()
            self.manageMetric = True
        else:
            self.metric       = metric
            self.manageMetric = False
        self.period = period
        self.stdev  = stdev
        self.sma    = SimpleMovingAverage(metric=self.metric, period=period)
        self.data   = list()

    def value(self):
        if self.ready() == False:
            return None
        arr = numpy.array(self.data)
        return numpy.std(arr) * self.stdev

    def upperBand(self):
        if self.ready() == False:
            return None
        return self.sma.value() + self.value()

    def lowerBand(self):
        if self.ready() == False:
            return None
        return self.sma.value() - self.value()

    def movingAverage(self):
        return self.sma.value()

    def percentB(self):
        if self.ready() == False:
            return None
        sma = self.sma.value()
        x = self.metric.value()
        bb = self.value()
        # range is 2x bb, so %b (0 at bottom) is (x-(sma-bb))/(2*bb)
        # note 2 here is unrelated to stdev multiplier but because
        # we have 2 bands, upper and lower
        v = (x - (sma-bb))
        if v == 0 or bb == 0:
            return 0
        return v/(2*bb)

    def ready(self):
        if len(self.data) >= self.period:
            return True
        return False

    def handle(self, periodData):
        if self.manageMetric:
            self.metric.handle(periodData)
        self.sma.handle(periodData)
        if self.sma.ready():
            deviation = self.metric.value() - self.sma.value()
            self.data.append(deviation);
            if len(self.data) > self.period:
                self.data = self.data[(len(self.data)-self.period):]

    def recommendedPreload(self):
        return self.period*2

# just a wrapper so we can use PercentB with the Historic Metric, which wants to use the value() call
class BollingerBandsPercentB(Metric):
    def __init__(self, period=20, stdev=2.0, metric=None):
        self.bb = BollingerBands(period=period, stdev=stdev, metric=metric)

    def value(self):
        if self.bb.ready() == False:
            return None
        return self.bb.percentB()

    def ready(self):
        return self.bb.ready()

    def handle(self, periodData):
        self.bb.handle(periodData)

    def recommendedPreload(self):
        return self.bb.recommendedPreload()

# Formula from Wilder's book, or see here
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
# Note that Investopedia's definition is WRONG
class RSI(Metric):
    def __init__(self, period=14, metric=None):
        if metric == None:
            self.metric = Close()
            self.manageMetric = True
        else:
            self.metric=metric
            self.manageMetric = False
        self.initgains = list()
        self.initlosses = list()
        self.averageGain=None
        self.averageLoss=None
        self.lastVal = None
        self.rsi = None
        self.period=period

    def value(self):
        return self.rsi

    def ready(self):
        if self.rsi != None:
            return True
        return False

    def handle(self, periodData):
        if self.manageMetric:
            self.metric.handle(periodData)
        if self.metric.ready():
            val = self.metric.value()
            if self.lastVal != None:
                delta = val - self.lastVal
                gain = max(0.0,delta)
                loss = max(0.0, -1.0*delta)
                if self.initgains != None:
                    self.initgains.append(gain)
                else:
                    self.averageGain = ((self.averageGain*(float(self.period-1))) + gain)/float(self.period)
                if self.initlosses != None:
                    self.initlosses.append(loss)
                else:
                    self.averageLoss = ((self.averageLoss*(float(self.period-1))) + loss)/float(self.period)
                if self.initgains != None and len(self.initgains) == self.period:
                    self.averageGain = sum(self.initgains)/float(self.period)
                    self.initgains = None
                if self.initlosses != None and len(self.initlosses) == self.period:
                    self.averageLoss = sum(self.initlosses)/float(self.period)
                    self.initlosses = None
                if self.averageGain != None and self.averageLoss != None:
                    if self.averageGain == 0 and self.averageLoss == 0:
                        self.rsi = 50
                    elif self.averageGain == 0:
                        self.rsi = 0
                    elif self.averageLoss == 0:
                        self.rsi = 100
                    else:
                        rs = self.averageGain/self.averageLoss
                        self.rsi = 100 - (100/(1+rs))
            self.lastVal = val

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + (self.period*2)

class LogN(Metric):
    def __init__(self, metric):
        self.metric = metric
        self.val = None

    def ready(self):
        return self.metric.ready()

    def value(self):
        return self.val

    def handle(self, perioddata):
        if self.metric.ready():
            self.val = log(self.metric.value())

    def recommendedPreload(self):
        return self.metric.recommendedPreload()

class STDev(Metric):
    def __init__(self, metric, period):
        self.metric = metric
        self.period=period
        self.data = list()

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def value(self):
        if self.ready():
            return numpy.std(self.data)
        return None

    def handle(self, perioddata):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data) > self.period:
                self.data = self.data[len(self.data)-self.period:]

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

# NOTE not annualized! dependent on data period - could work it in
class HistoricVolatility(Metric):
    def __init__(self, period=100, metric=None):
        if metric == None:
            self.metric = Close()
            self.manageMetric=True
        else:
            self.metric = metric
            self.manageMetric = False
        self.historicmetric = HistoricMetric(self.metric,1)
        self.div = Divide(self.metric, self.historicmetric)
        self.xi = LogN(self.div)
        self.xistd = STDev(self.xi,period)
        self.dataperiod = None

    def ready(self):
        return self.xistd.ready()

    def value(self):
        ret = self.xistd.value()
        days = float(self.dataperiod) / 86400.0
        # comp for weekends
        days = (7.0/5.0)*days
        return ret * (sqrt(252))

    def handle(self, perioddata):
        if self.dataperiod != None and self.dataperiod != perioddata.period:
            raise ValueError("HistoricVolatility was passed data with differing time intervals")
        self.dataperiod = perioddata.period
        if self.manageMetric:
            self.metric.handle(perioddata)
            self.historicmetric.handle(perioddata)
            self.div.handle(perioddata)
            self.xi.handle(perioddata)

    def recommendedPreload(self):
        return self.xistd.recommendedPreload()

class NumTaps(Metric):
    def __init__(self, metric, period, margin):
        self.metric=metric
        self.period=period
        self.margin=margin
        self.data = list()

    def value(self):
        if self.ready() == False:
            return None
        retval = 0
        high = max(self.data)
        for x in self.data:
            if (high - x) <= self.margin:
                retval = retval + 1
        return retval

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period

class NumTapsShort(Metric):
    def __init__(self, metric, period, margin):
        self.metric=metric
        self.period=period
        self.margin = margin
        self.data = list()

    def value(self):
        retval = 0
        if self.ready() == False:
            return None
        floor = min(self.data)
        for x in self.data:
            if (x-floor) <= self.margin:
                retval = retval + 1
        return retval

    def ready(self):
        if len(self.data) < self.period:
            return False
        return True

    def handle(self, periodData):
        if self.metric.ready():
            self.data.append(self.metric.value())
            if len(self.data)>self.period:
                self.data.pop(0)

    def recommendedPreload(self):
        return self.metric.recommendedPreload() + self.period
