
from indicators import MultiMetricMetric, AdjustedATR, STDev, AdjustedClose


class CarterSqueeze(MultiMetricMetric):
    def __init__(self):
        MultiMetricMetric.__init__(self)
        self.close = AdjustedClose()
        self.stdev = STDev(metric=self.close, period=20)
        self.atr = AdjustedATR(period=20)
        self._addMetrics(self.close, self.stdev, self.atr)

    def value(self):
        # Keltner minus bb width, <=0 means squeeze is on
        return (self.atr.value() * 1.5) - (self.stdev.value() * 2)
