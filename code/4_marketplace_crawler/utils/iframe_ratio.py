import pandas as pd
import os
import sys

count=0
countmp=0
countmpi=0

#read path from cli
path = sys.argv[1]
files = os.listdir(path)

for file in files:
    if "iframe" in file:
        count+=1
ratio=count/(len(files)-count)

print("Total number of files are  :"+str(len(files)))
print("Total ifarmes captured are :"+str(count))
print("Global ratio of iframe capture is :" +str(ratio))
print()

list_mps = ["poki",
            "crazygames",
            "y8",
            "miniclip",
            "friv",
            "vseigru",
            "ufreegames",
            "coolmathgames",
            "fukgames",
            "spiels",
            "iogame",
            "addictinggames",
            "gameflare",
            "mousebreaker",
            "webgameapp",
            "yourgames",
            "yupi",
            "yad",
            "babygames",
            "kibagames",
            "itch" ]

for mp in list_mps:
    for file in files:
        if mp in file:
            countmp+=1
        if mp+"_iframe" in file:
            countmpi+=1
    # print("Total number of files for "+mp+ " is " + str(countmp))
    # print("Total numer of iframes for "+mp+" is " + str(countmpi))
    ratio=countmpi/(countmp-countmpi)
    print("ratio of iframe capture for " +mp+ " is " + str(ratio))
