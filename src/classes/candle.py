
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
