import datetime
import json
now = datetime.datetime.now()

with open('westJesTimes.json', 'r') as openfile:
    times = json.load(openfile)
# small bug where the timetable shows times just past midnight as part of the day before
if now.weekday() == 5:
    day = "Saturday"
elif now.weekday() == 6:
    day = "Sunday"
else:
    day = "Weekday"
lowest=[{"diff":9999}]*4
print(lowest)
currentTime = now.hour*60 + now.minute
for i in times[day]:
    testTime = int(i["Time"][0:2])*60+int(i["Time"][2:4])
    if currentTime<testTime:
        diff = testTime - currentTime

        if diff < lowest[-1]["diff"]:
            lowest.append({"rec":i,"diff":diff})
            lowest = sorted(lowest, key=lambda d: d['diff'])[:-1]
print(lowest)     
for i in lowest:   
    print(i["rec"]["Terminates"],i["diff"])