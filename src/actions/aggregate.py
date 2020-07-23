import sys
from src.classes.candle import candle

candlesticks = {}

def aggregate(trade):
    if trade.timestamp not in candlesticks:     #first candle of that timestamp interval
        print("Timestamp,side,size,price,grossValue,homeNotional,foreignNotional   - Timestamp,Open,High,Low,Close,Vol (Present Candle)")
        c = candle(trade.timestamp,trade.price, trade.price, trade.price, trade.price, trade.homeNotional)
        candlesticks[trade.timestamp] = c
        if ("test" in sys.argv):                          #test mode - used for CI
            if c.open > 0 and c.high > 0 and c.low > 0 and c.close > 0 and c.volume > 0 :
                print("Test OK")
                exit(0)
    else:
        if trade.price > candlesticks[trade.timestamp].high:
            candlesticks[trade.timestamp].high = trade.price
        elif trade.price < candlesticks[trade.timestamp].low:
            candlesticks[trade.timestamp].low = trade.price

    candlesticks[trade.timestamp].close = trade.price
    candlesticks[trade.timestamp].addVolume(trade.homeNotional)
    print( '< {:<65s} - {:<65s}'.format(str(trade), str(candlesticks[trade.timestamp]) ) )
