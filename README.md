# indicators

This is a python library and supporting files for calculating various technical indicators used
in trading markets.  It builds on code from my stocklib module also in github.  you feed an 
indicator a time series of data 1 bar at a time and it continuously updates it's value.  I use 
this personally, but it will likely require some effort for other people to put it to use.

Take a look at stocklib first and get that to work before making use of this code.

## Dependencies

indicators uses depends on my stocklib code and on numpy.  If you are pulling historic data out of
MySQL (likely if you use stocklib as-is) then you will also need MySQL-python.  There are a number
of other web-scraping related dependencies in stocklib for scraping Yahoo/etc data so check the
stocklib README.md for details.

* `pip install numpy`

## Useage

pending
