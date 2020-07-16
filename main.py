import sys
import websocket
import json
import pandas as pd

#### In close is not printing the dictionary elements propperly, check if it's storing them propperly
#### Continue using: https://blog.quantinsti.com/tick-tick-ohlc-data-pandas-tutorial/
#### wscat -c wss://www.bitmex.com/realtime


# Symbol we are ask¡ng data for
symbol= "XBTUSD"
webSocketURL="wss://www.bitmex.com/realtime"
candlesticks = {}
interval = "1m"

class trade:
    def __init__(self, timestamp, side, size, price, grossValue, homeNotional, foreignNotional):
        self.timestamp = timestamp
        self.side = side
        self.size = size
        self.price = price
        self.grossValue = grossValue
        self.homeNotional = homeNotional
        self.foreignNotional = foreignNotional

    def __str__(self):
        return (f"{self.timestamp},{self.side},{self.size},{self.price},{self.grossValue},{self.homeNotional},{self.foreignNotional}")

class candle:
    def __init__(self, timestamp, o, h, l, c, v):
        self.timestamp = timestamp
        self.open = o
        self.high = h
        self.low = l
        self.close = c
        self.volume = v

    def __str__(self):
        return (f"{self.timestamp},{self.open},{self.high},{self.low},{self.close},{self.volume}")

    def addVolume(self,v):
        self.volume += v

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


def addTrade(t):
    if interval == "1m":     # leave just minutes timestamps and call aggregate
        minuteTimestamp= t.timestamp.split(":",2)[0] + ":" + t.timestamp.split(":",2)[1]
        t.timestamp = minuteTimestamp
        aggregate(t)
    elif interval == "5m":   # leave just five minutes timestamps and call aggregate
        minutes = int(t.timestamp.split(":",2)[1]) % 10
        if (minutes >= 0 and minutes <= 4):
            minutes = 0
        else:
            minutes = 5
        ten = t.timestamp.split(":",2)[1][:-1]   # leave the ten part
        fiveMinTimestamp = t.timestamp.split(":",2)[0] + ":" + ten + str(minutes)
        t.timestamp = fiveMinTimestamp
        aggregate(t)


try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    tmp = json.loads(message)

    if ("data" in tmp):
        # get the data from the json received
        data= tmp["data"][0]
        # discard miliseconds
        
        addTrade(trade(data["timestamp"],data["side"],data["size"],data["price"],data["grossValue"], \
                       data["homeNotional"],data["foreignNotional"]))


    elif ("success" in tmp):
        print(f"- Suscribed successfully to {symbol}> Sending:  {tmp})")
        print(f"- Receiving and aggregating for interval {interval}:")


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("- Closed connection")

def on_open(ws):
    def run(*args):
        print("- Subscribing to " + symbol)
        ws.send('{"op": "subscribe", "args": ["trade:' + symbol + '"]}')
    thread.start_new_thread(run, ())
    print("------------------------------------------------------------")


if __name__ == "__main__":

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(webSocketURL,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    print(f"\nCandlesticks:\n    Timestamp   , Open, High, Low, Close, Volume")
    for key, value in candlesticks.items():
        print(value)    #this constitutes a candlestick or line