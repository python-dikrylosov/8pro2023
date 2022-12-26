import yfinance as yf
import time
import math
import numpy as np

real_time = str(time.strftime("%Y-%m-%d"))

dfuid = yf.download("AXS-BTC",start="2014-01-01",end=real_time,interval="1d")

print(dfuid)
