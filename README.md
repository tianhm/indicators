# indicators

This is a python library and supporting files for calculating various technical indicators used
in trading markets.  It builds on code from my `stocklib` module also in github.  You feed an
indicator a time series of data 1 bar at a time and it continuously updates it's value.  I use
this personally, but it will likely require some effort for other people to put it to use.

Take a look at `stocklib` first and get that to work before making use of this code.

## Dependencies

`indicators` uses depends on my `stocklib` code and it's dependencies.

## Useage

The indicators code is split between Checks and Metrics.

### Check

A `Check` takes a stream of bar data and indicates a simple `True`/`False` value.  For example, you might write a custom `Check` to indicate if
the last close price was above a moving average or if average volume was above 500,000 shares.  All `Checks` should
inherit from the `Check` class.  Here is a simple example using a check:

    check = MyTrendCheck()
    for periodData in generate_random_series():
        check.handle(periodData)

        if check.ready():
            if check.check():
                print "%s passed" % (periodData.date,)

### Metric

A `Metric` takes a stream of bar data and calculates a numeric float value.  This is where concepts
like MACD, Stochastics, Bollinger Bands and Moving Averages live.

    close = AdjustedClose()
    sma = SimpleMovingAverage(metric=close, period=20)

    print "Date,SMA"

    for periodData in generate_random_series():
        close.handle(periodData)
        sma.handle(periodData)

        if sma.ready() and close.ready():
            print "%s,%f" % (periodData.date, sma.value())
