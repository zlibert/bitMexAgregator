try:
    import thread
except ImportError:
    import _thread as thread

# Symbol we are asking data for
symbol= "XBTUSD"

def on_open(ws):
    def run(*args):
        print("- Subscribing to " + symbol)
        ws.send('{"op": "subscribe", "args": ["trade:' + symbol + '"]}')
    thread.start_new_thread(run, ())
    print("-"*30)
