import metro
import datetime

now = datetime.datetime.now()
g = metro.nextTrains(now.weekday(), now.hour*60 + now.minute,5)

# time = 1*60 + 55
# print(time)
# g = metro.nextTrains(now.weekday(), time,5)
print("GOT:")
print(g)
metro.printResult(g)
