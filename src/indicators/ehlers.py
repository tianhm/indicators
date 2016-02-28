from indicators import MultiMetricMetric, AdjustedClose, AdjustedHigh, AdjustedLow, Highest, Lowest


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
