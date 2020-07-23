import json
from src.actions.addTrade import addTrade
from src.classes.trade import trade

symbol= "XBTUSD"
interval = "1m"

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
