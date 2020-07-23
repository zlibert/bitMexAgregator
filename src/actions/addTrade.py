from src.actions.aggregate import aggregate

interval = "1m"

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
