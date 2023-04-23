import json
with open('westJesTimes.json', 'r') as openfile:
    times = json.load(openfile)

# day is an int from 0-6 (Mon 0, Tue 1...)
# time is the number of seconds since midnight ( hours*60 + mintues)
# n is the number of results to return
def nextTrains(day, time,n):

    # if its in the first hour of the morning treat it as if it was the day before
    if time < 60:
        day = day - 1

    # converts the day number to the day in words 
    if day == 5:
        day = "Saturday"
    elif day == 6:
        day = "Sunday"
    else:
        day = "Weekday"
    lowest=[{'rec': {'Time': '0000', 'Line': 'NONE', 'Terminates': 'NONE', 'dir': 0}, 'diff': 999}]*n
    currentTime = time
    for i in times[day]:
        # adjust for times after midnight
        if i["Time"][0:2] == "00":
           hour = 24
        else:
            hour = int(i["Time"][0:2])

        testTime = hour*60+int(i["Time"][2:4])
        if currentTime<testTime:
            diff = testTime - currentTime
            if diff < lowest[-1]["diff"]:
                lowest.append({"rec":i,"diff":diff})
                lowest = sorted(lowest, key=lambda d: d['diff'])[:-1]   

    return lowest
def printResult(r):
    for i in r:   
        print(i["rec"]["Terminates"],i["diff"])

def shortenResult(r):
    """Takes the result from nextTrains and shortens the staion names.
    """
    o = []
    for i in r:
        if i["rec"]["Terminates"] == "South Hylton":
            e = i
            e["rec"]["Terminates"] = "S.Hylton"
            o.append(e)
        elif i["rec"]["Terminates"] == "South Shields":
            e = i
            e["rec"]["Terminates"] = "S.Shields"
            o.append(e)
        # elif i["rec"]["Terminates"] == "Park Lane":
        #     e = i
        #     e["rec"]["Terminates"] = "Park ln"
        #     o.append(e)
        elif i["rec"]["Terminates"] == "Monument via Whitley Bay":
            e = i
            e["rec"]["Terminates"] = "Mon via cst"
            o.append(e)
        elif i["rec"]["Terminates"] == "Regent Centre":
            e = i
            e["rec"]["Terminates"] = "Regent cen"
            o.append(e)
        else:
            o.append(i)
    return o