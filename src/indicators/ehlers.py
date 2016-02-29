from indicators import Metric, MultiMetricMetric, AdjustedClose, AdjustedHigh, AdjustedLow, Highest, Lowest


class Fisher(MultiMetricMetric):
    def __init__(self, period):
        MultiMetricMetric.__init__(self)

        self.close = AdjustedClose()
        self.period = period
        self.high = AdjustedHigh()
        self.low = AdjustedLow()
        self.highest = Highest(self.high, period)
        self.lowest = Lowest(self.low, period)
        self.lastValue = 0

        self._addMetrics(self.close, self.high, self.low, self.highest, self.lowest)

    def value(self):
        if not self.ready():
            return 0
        v = 0.5 * 2 * ((self.close.value() - self.lowest.value()) /
                       (self.highest.value() - self.lowest.value()) - 0.5) \
            + 0.5 * self.lastValue
        self.lastValue = v
        return v


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