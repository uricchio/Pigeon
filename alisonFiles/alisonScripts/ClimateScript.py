import sys

def loadClimAvg(fileName):
    climDataAvg = []
    fh = open(fileName)
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
            
        climDataAvg.append(small_arr)
    return(climDataAvg)  
    

#import pandas as pd

#def tableClimAvg(fileName):
#   dataAvg= pd.read_csv(fileName)



def loadClimExtreme(fileName):
    climDataExtreme = []
    fh = open(fileName)
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
            
        climDataExtreme.append(small_arr)
    return(climDataExtreme)  

    
# import pandas as pd

#def tableClimExtreme(fileName)
#   dataExtreme = pd.read_csv(fileName)
