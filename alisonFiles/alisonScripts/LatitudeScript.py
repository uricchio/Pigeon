import sys

def loadLat(LatfileName):
    latData = []
    fh = open(LatfileName)
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
            
        latData.append(small_arr)
    return(latData)