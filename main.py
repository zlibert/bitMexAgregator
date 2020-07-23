import websocket
from src.events.on_message import on_message
from src.events.on_error import on_error
from src.events.on_close import on_close
from src.events.on_open import on_open
import time

#### In close is not printing the dictionary elements propperly, check if it's storing them propperly
#### Continue using: https://blog.quantinsti.com/tick-tick-ohlc-data-pandas-tutorial/
#### wscat -c wss://www.bitmex.com/realtime
candlesticks = {}
webSocketURL="wss://www.bitmex.com/realtime"

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