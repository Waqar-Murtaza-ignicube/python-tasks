"""module datetime to get format object and colored to get colored object for console"""

from datetime import datetime
from termcolor import colored

year = input("Enter a year to find the highest, lowest temperate, and humditiy with day: ")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Oct", "Nov", "Dec"]

#global variables for appending the list with temp and humid
maxTemp = []
lowTemp = []
maxHumid = []
Index = []

for i in months:
    with open(f"weatherdata/lahore_weather_{year}_{i}.txt", encoding="utf-8") as openFile:
        reportFile = openFile.readlines()
        if reportFile and len(reportFile) > 1 and not reportFile[0].strip():
            reportFile = reportFile[2:-1]
            for j in reportFile:
                temp = j.split(",")
                if temp[1] == "":
                    continue
                if temp[3] == "":
                    continue
                if temp[7] == "":
                    continue
                maxTemp.append(int(temp[1]))
                lowTemp.append(int(temp[3]))
                maxHumid.append(int(temp[7]))
                Index.append(temp[0])

# calculating highest temp, humid and lowest temp from the list we made
MAXTEMPINDEX = 0
initMaxTemp = maxTemp[0]
for i, maxTempp in enumerate(maxTemp):
    initMaxTemp = max(initMaxTemp, maxTempp)
    MAXTEMPINDEX = maxTemp.index(initMaxTemp)

MAXHUMIDINDEX = 0
initHumid = maxHumid[0]
for i, maxHumidd in enumerate(maxHumid):
    initHumid = max(initHumid, maxHumidd)
    MAXHUMIDINDEX = maxHumid.index(initHumid)

LOWTEMPINDEX = 0
initLowTemp = lowTemp[0]
for i, lowTempp in enumerate(lowTemp):
    initLowTemp = min(initLowTemp, lowTempp)
    LOWTEMPINDEX = lowTemp.index(initLowTemp)

# Convert date string to the desired format
DATE_FORMAT = "%Y-%m-%d"
mtfDate = datetime.strptime(Index[MAXTEMPINDEX], DATE_FORMAT).strftime("%B %d")
ltfDate = datetime.strptime(Index[LOWTEMPINDEX], DATE_FORMAT).strftime("%B %d")
mhfDate = datetime.strptime(Index[MAXHUMIDINDEX], DATE_FORMAT).strftime("%B %d")

# printing the result
print(f"Highest: {initMaxTemp}C on {mtfDate}")
print(f"Lowest: {initLowTemp}C on {ltfDate}")
print(f"Humid: {initHumid}% on {mhfDate}")

#calculating on the basis of month
month = input("Enter a month (i.e: Jan, Feb, Apr etc) to display the average highest temperature"
", average lowest temperature, average humidity: ")

avgMaxTemp = []
avgLowTemp = []
avgMaxHumid = []
monMaxTemp = []
monLowTemp = []
monIndex = []

with open(f"weatherdata/lahore_weather_{year}_{month}.txt", encoding="utf-8") as openFile:
    reportFile = openFile.readlines()
    if reportFile and len(reportFile) > 1 and not reportFile[0].strip():
        reportFile = reportFile[2:-1]
        for i in reportFile:
            temp = i.split(",")
            #checking if the column has an empty value/string
            if temp[2] == "":
                continue
            if temp[8] == "":
                continue
            if temp[1] == "":
                continue
            if temp[3] == "":
                continue
            if temp[7] == "":
                continue
            monMaxTemp.append(int(temp[1]))
            monLowTemp.append(int(temp[3]))
            maxHumid.append(int(temp[7]))
            avgMaxTemp.append(int(temp[2]))
            avgLowTemp.append(int(temp[2]))
            avgMaxHumid.append(int(temp[8]))
            monIndex.append(temp[0])


    #calculating highest temp, humid and lowest temp from the list we made
    initAvgMaxTemp = avgMaxTemp[0]
    for i, avgMaxTempp in enumerate(avgMaxTemp):
        initAvgMaxTemp = max(initAvgMaxTemp, avgMaxTempp)

    initAvgHumid = avgMaxHumid[0]
    for i, avgMaxHumidd in enumerate(avgMaxHumid):
        initAvgHumid = max(initAvgHumid, avgMaxHumidd)

    initAvgLowTemp = avgLowTemp[0]
    for i, avgLowTempp in enumerate(avgLowTemp):
        initAvgLowTemp = min(initAvgLowTemp, avgLowTempp)

    MAXTEMPINDEX = 0
    initMaxTemp = monMaxTemp[0]
    for i, monMaxTempp in enumerate(monMaxTemp):
        initMaxTemp = max(initMaxTemp, monMaxTempp)
        MAXTEMPINDEX = monMaxTemp.index(initMaxTemp)

    initLowTemp = monLowTemp[0]
    for i, monLowTempp in enumerate(monLowTemp):
        initLowTemp = min(initLowTemp, monLowTempp)

    # printing the result
    print(f"Highest Average: {initAvgMaxTemp}C ")
    print(f"Lowest Average: {initAvgLowTemp}C ")
    print(f"Average Humidity: {initAvgHumid}% ")

    DATE_FORMAT = "%Y-%m-%d"

    mtfDate = datetime.strptime(monIndex[MAXTEMPINDEX], DATE_FORMAT).strftime("%B %Y")
    print(mtfDate)

    dayIndex = []
    for h in monIndex:
        ltfDate = datetime.strptime(h, DATE_FORMAT).strftime("%d")
        dayIndex.append(ltfDate)

    #printing the horizontal bar chart with colors
    for j, k, l in zip(dayIndex, monMaxTemp, monLowTemp):
        print(f"{j} {colored('+' * k, 'red')} {k:2}C")
        print(f"{j} {colored('+' * l, 'blue')} {l:1}C")

    for j, k, l in zip(dayIndex, monMaxTemp, monLowTemp):
        print(f"{j} {colored('+' * l, 'blue')}{colored('+' * k, 'red')} {l:1}C - {k:2}C")
