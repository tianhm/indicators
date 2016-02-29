from indicators import Metric, MultiMetricMetric, AdjustedClose,\
    AdjustedHigh, AdjustedLow, Highest, Lowest, Add, Divide, Value
from math import log


class TOSFisher(MultiMetricMetric):
    def __init__(self, period):
        MultiMetricMetric.__init__(self)

        self.close = AdjustedClose()
        self.period = period
        self.high = AdjustedHigh()
        self.low = AdjustedLow()
        self.p1 = Add(self.high, self.low)
        self.price = Divide(self.p1, Value(2))
        self.highest = Highest(self.price, period)
        self.lowest = Lowest(self.price, period)
        self.val = 0
        self.fish = 0

        self._addMetrics(self.close, self.high, self.low, self.p1, self.price,
                         self.highest, self.lowest)

    def handle(self, perioddata):
        MultiMetricMetric.handle(self, perioddata)

        if self.ready():
            self.val = 0.66 * ((self.price.value() - self.lowest.value()) /
                               (self.highest.value() - self.lowest.value()) - 0.5) \
                       + 0.67 * self.val
            if self.val > .9999:
                self.val = .9999
            if self.val < -.9999:
                self.val = -.9999

            self.fish = 0.5 * (log((1 + self.val) / (1 - self.val)) + self.fish)

    def value(self):
        return self.fish


class Fisher(MultiMetricMetric):
    def __init__(self, period):
        MultiMetricMetric.__init__(self)

        self.close = AdjustedClose()
        self.period = period
        self.high = AdjustedHigh()
        self.low = AdjustedLow()
        self.p1 = Add(self.high, self.low)
        self.price = Divide(self.p1, Value(2))
        self.highest = Highest(self.price, period)
        self.lowest = Lowest(self.price, period)
        self.lastValue = 0
        self.lastFish = 0

        self._addMetrics(self.close, self.high, self.low, self.p1, self.price,
                         self.highest, self.lowest)

    def value(self):
        if not self.ready():
            return 0
        v = 0.5 * 2 * ((self.price.value() - self.lowest.value()) /
                       (self.highest.value() - self.lowest.value()) - 0.5) \
            + 0.5 * self.lastValue
        if v > .9999:
            v = .9999
        if v < -.9999:
            v = -.9999
        self.lastValue = v

        fish = 0.25 * log((1+v)/(1-v)) + 0.5 * self.lastFish

        self.lastFish = fish
        return fish



class InstantaneousTrendline(Metric):
    def __init__(self, alpha):
        Metric.__init__(self)
        self.alpha = alpha
        self.it = 0
        self.it1 = 0
        self.it2 = 0
        self.price = 0
        self.price1 = 0
        self.price2 = 0

    def handle(self, perioddata):
        self.it2 = self.it1
        self.it1 = self.it
        self.price2 = self.price1
        self.price1 = self.price

        self.price = perioddata.adjustedClose
        self.it = (self.alpha-((self.alpha/2)*(self.alpha/2))) * self.price + ((self.alpha*self.alpha)/2)*self.price1 \
            - (self.alpha-(3*(self.alpha*self.alpha))/4)*self.price2 + 2*(1-self.alpha)*self.it1 \
            - ((1-self.alpha)*(1-self.alpha))*self.it2

    def ready(self):
        if self.price2 != 0:
            return True
        return False

    def value(self):
        return self.it