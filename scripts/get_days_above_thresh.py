import sys
import re

fh=open(sys.argv[1],'r')
thresh = float(sys.argv[2])

daysAbove={}
daysAboveMin1={}
daysTot = {}

# skip first line
for line in fh:
    break

# get temp data
for line in fh:
    line = line.strip()
    line=line.replace("\",\"","*")
    data=line.split("*")
 
    if len(data) < 4:
        continue
 
    month = int(data[2][5:7])
    if month < 4 or month > 10:
        continue
    year = int(data[2][0:4])	
    temp = float(data[3][:-1])
   
    if year not in daysAbove:
        daysAbove[year] = 0
        daysAboveMin1[year] = 0
        daysTot[year] = 0

    if temp > thresh:
        daysAbove[year] += 1

    if temp > thresh-5:
        daysAboveMin1[year] += 1
    
    daysTot[year] += 1

for year in daysAbove:
    if daysTot[year] > 200:
        print (year, daysAbove[year]/daysTot[year], daysAboveMin1[year]/daysTot[year])

