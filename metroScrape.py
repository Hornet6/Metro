import requests

URL = "https://www.nexus.org.uk/metro/timetables-and-stations/west-jesmond/timetable"
page = requests.get(URL)
times = {}
days = ["Monday to Friday","Saturday","Sunday"]
dayCode = ["Weekday","Saturday","Sunday"]
for i in range(len(days)):
    times[dayCode[i]] = []

lineLookup={"Airport":"Green","South Hylton":"Green","South Shields":"Yellow","St James":"Yellow"}
dirSearch={"Airport":"Towards Airport","South Hylton":"Towards South Hylton","South Shields":"Towards South Shields","St James":"Towards St James"}
directions = ["South Shields","South Hylton","St James","Airport"]
directionLoc = page.text.find(dirSearch[directions[0]])
count=0
for dir in range(0,4):
    if dir==3:
        nextDirLoc = len(page.text)-1
    else:
        nextDirLoc = page.text.find(dirSearch[directions[dir+1]],directionLoc+1)
    if directionLoc == -1:
        pass
    d=0
    dayLoc = page.text.find(days[d],directionLoc)
    print("DAYLOC:",dayLoc,nextDirLoc,dayLoc < nextDirLoc,d)
    while dayLoc < nextDirLoc and d<3:
        if d==2:
            nextDayLoc = nextDirLoc
        else:
            nextDayLoc = page.text.find(days[d+1],dayLoc)
        hourLoc = page.text.find("tbl-content-item bg-secondary",dayLoc)
        nextHourLoc = page.text.find("tbl-content-item bg-secondary",hourLoc+5)
        while hourLoc<nextDayLoc and hourLoc !=-1:
            hour = page.text[hourLoc+31:hourLoc+33]
            nextHourLoc = page.text.find("tbl-content-item bg-secondary",hourLoc+5)
            minLoc = hourLoc+31
            minLoc = page.text.find("tbl-content-item",minLoc+10)
            while minLoc<nextHourLoc and minLoc != -1:
                count+=1
                min = page.text[minLoc+18:minLoc+20]
                times[dayCode[d]].append({"Time":hour+min,"Line":lineLookup[directions[dir]],"Terminates":directions[dir],"dir":dir})
                minLoc = page.text.find("tbl-content-item",minLoc+10)
            hourLoc = nextHourLoc
        d+=1
        if d<3:
            dayLoc = page.text.find(days[d],directionLoc)
    directionLoc = nextDirLoc
# print(times)

import json
jobject = json.dumps(times, indent=4)
with open("westJesTimes.json", "w") as outfile:
    outfile.write(jobject)
print("Weekday:") 
print(len(times["Weekday"]))
print("Saturday:") 
print(len(times["Saturday"]))
print("Sunday:") 
print(len(times["Sunday"]))
print("Count")
print(count)
# with open("westJesTimes.json", "w") as outfile:
#     outfile.write("TEST")
