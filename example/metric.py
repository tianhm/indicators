'''
Example Metric code

@author: oly
'''
from indicators.indicators import SimpleMovingAverage, AdjustedClose
from random import random
from stocklib.perioddata import PeriodData, Period
from datetime import datetime, timedelta

# Helper functons to create some fake financial data
# TODO I duplicated this for check code, so put it in a util module next time I am in here
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

# Here begins the example code

# Track the adjusted close and 20 period simple moving average 
close = AdjustedClose()
sma = SimpleMovingAverage(metric=close, period=20)

print "Date,SMA"

for periodData in generate_random_series():
    close.handle(periodData)
    sma.handle(periodData)
    
    if sma.ready() and close.ready():
        print "%s,%f" % (periodData.date, sma.value())
