import requests
import json

# function takes a station name in the format for its URL, a list of these is in metro station.txt
# it goes to the page and scrapes the timeable
# it then writes it to a json file called stationName.json
def lookup(stationName): 
    URL = "https://www.nexus.org.uk/metro/timetables-and-stations/"+stationName+"/timetable"
    print(URL)
    page = requests.get(URL)
    times = {}
    days = ["Monday to Friday","Saturday","Sunday"]
    dayCode = ["Weekday","Saturday","Sunday"]
    for i in range(len(days)):
        times[dayCode[i]] = []

    lineLookup={"Airport":"Green","South Hylton":"Green","South Shields":"Yellow","St James":"Yellow"}
    # dirSearch={"Airport":"Towards Airport","South Hylton":"Towards South Hylton","South Shields":"Towards South Shields","St James":"Towards St James"}
    # directions = ["South Shields","South Hylton","St James","Airport"]
    # directionLoc = page.text.find(dirSearch[directions[0]])

    # this finds the destination of a table
    directionLoc = page.text.find("Towards")

    # most cases will just find the start of the closing tag
    # however in the case where it goes via, we shorten it:
    # St James via Whitley Bay -> St James

    # could use the min function here
    terminusEnd = page.text.find("<",directionLoc)
    if page.text.find("via",directionLoc) < terminusEnd and page.text.find(" via ",directionLoc) != -1:
        terminusEnd = page.text.find(" via ",directionLoc)
    terminusName = page.text[directionLoc+8:terminusEnd]

    nextTerminusName = "NONE"
    count=0
    for dir in range(0,4):
        diffTerm=[]

        # this gets the location of the start of the next table so that we know the location of the end of the current table
        nextDirLoc = page.text.find("Towards",directionLoc+1)
        if nextDirLoc == -1:
            nextDirLoc = len(page.text)-1
        else:
            terminusEnd = page.text.find("<",nextDirLoc)
            # this fixes an edge case where the trains to to somewhere via somewhere else
            if page.text.find(" via ",nextDirLoc) < terminusEnd and page.text.find(" via ",nextDirLoc) != -1:
                terminusEnd = page.text.find(" via ",nextDirLoc)
            nextTerminusName = page.text[nextDirLoc+8:terminusEnd]

        if directionLoc == -1:
            pass
        d=0
        dayLoc = page.text.find(days[d],directionLoc)
        # print("DAYLOC:",dayLoc,nextDirLoc,dayLoc < nextDirLoc,d)
        # for each of the different days (Weekday, Saturday, Sunday)
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
                    # this checks if the train has a different terminus and adds it to diff term if it does
                    # this is delt with below
                    if page.text[minLoc+33:minLoc+56] == 'class="terminates_item"':
                        diffTerm.append({"dayCode":dayCode[d], "number":len(times[dayCode[d]]) ,"letter":page.text[minLoc+57:minLoc+58]})

                    times[dayCode[d]].append({"Time":hour+min,"Line":lineLookup[terminusName],"Terminates":terminusName,"dir":dir})
                    minLoc = page.text.find("tbl-content-item",minLoc+10)
                hourLoc = nextHourLoc
            d+=1
            if d<3:
                dayLoc = page.text.find(days[d],directionLoc)



        # this code manages the trains that terminate at different places
        lookUpLetter = {}

        letterLoc = directionLoc
        while letterLoc < nextDirLoc:
            letterLoc = page.text.find('class="tbl-info-item-main"',letterLoc+1)
            if letterLoc == -1 or letterLoc >nextDirLoc:
                break
            # some of the trains with wierd terminus have different messages, such as 
            # "From Pelaw operates to South Shields"
            # while the normal messages look like:
            # "Terminates at Sunderland"
            
            termLoc = page.text.find('Terminates at ',letterLoc)

            if page.text.find(' to ',letterLoc) < termLoc or termLoc ==-1:
                
                termLoc = page.text.find(' to ',letterLoc)
                endOfEnd = page.text.find("<",termLoc+14)-1
                lookUpLetter[page.text[letterLoc+27:letterLoc+28]] = page.text[termLoc+4:endOfEnd+1]
            else:
                endOfEnd = page.text.find("<",termLoc+14)-1
                lookUpLetter[page.text[letterLoc+27:letterLoc+28]] = page.text[termLoc+14:endOfEnd]

        # This goes through and changes all of the terminus for the stations that end early
        for i in diffTerm:
            times[i["dayCode"]][i["number"]]["Terminates"] = lookUpLetter[i["letter"]]

        # set the current table location equal to the next table location
        directionLoc = nextDirLoc
        terminusName = nextTerminusName
    print(len(times["Weekday"]))
    print(len(times["Saturday"]))   
    print(len(times["Sunday"]))     
    jobject = json.dumps(times, indent=4)
    with open(stationName+".json", "w") as outfile:
        outfile.write(jobject)
    outfile.close()


# lookup("meadow-well")

# this goes through each of the stations in the file and creates a json file for each
# palmersville and shiremoor have been removed due to broken webpages
f = open("metro stations.txt", "r")
for x in f:
  print(x[:-1])
  lookup(x[:-1])


