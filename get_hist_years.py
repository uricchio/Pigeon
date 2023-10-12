import sys
import re

fh=open(sys.argv[1],'r')
year1 = int(sys.argv[2])
year2 = int(sys.argv[3])
temps = {}

temps[year1] = []
temps[year2] = []

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
 
    year = int(data[2][0:4])	
    temp = float(data[3][:-1])
   
    if year == year1 or year == year2:
        temps[year].append(temp)                

for year in temps:
    for temp in temps[year]:
        print(year, temp)

