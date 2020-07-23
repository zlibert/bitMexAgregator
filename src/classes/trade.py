
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
