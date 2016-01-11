'''
Example Check code

@author: oly
'''
from indicators.check import Check
from indicators.indicators import SimpleMovingAverage, AdjustedClose
from datetime import datetime, timedelta
from random import random
from stocklib.perioddata import PeriodData, Period

def generate_random_perioddata(dt):
    a = random()*50+50
    b = random()*50+50
    c = random()*50+50
    d = random()*50+50
    retval = PeriodData(date=dt,period=Period.DAILY, stock="AAPL", open=a,high=max((a,b,c,d)),low=min(a,b,c,d),close=d,volume=100000,adjustedClose=d)
    return retval

def generate_random_series():
    retval = list()
    dt = datetime(year=2015,month=1,day=1)
    for i in range(1000):
        dt = dt + timedelta(days=1)
        retval.append(generate_random_perioddata(dt))
    return retval

class MyTrendCheck(Check):
    def __init__(self):
        Check.__init__(self)
        # adjusted close accounts for splits and dividends
        self.close = AdjustedClose()
        self.ma = SimpleMovingAverage(metric=self.close, period=200)

    def handle(self, periodData):
        self.close.handle(periodData)
        self.ma.handle(periodData)
    
    def ready(self):
        return self.close.ready() and self.ma.ready()
    
    def check(self):
        if not self.ready():
            return False
        return self.close.value() > self.ma.value()

check = MyTrendCheck()
for periodData in generate_random_series():
    check.handle(periodData)
    
    if check.ready():
        if check.check():
            print "%s passed" % (periodData.date,)
