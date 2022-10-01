import os
import json
import numpy
import math
import time
import string
printable = set(string.printable)

def readStory():
    with open("STORY_IN.txt",'r') as file:
        lines=file.readlines()
    lines=[line.replace('\n','') for line in lines]
    return (" ".join(lines)).split(" ")

def binCount():
    return len([file for file in os.listdir("IO/BIN")])

def pauseRead():
    config=json.load(open("BRAIN.json"))
    config["Pause_Flag"]="1"
    with open("BRAIN.json","w") as outfile:
        outfile.write(json.dumps(config))
    return config

def main():

    words=readStory()
    
    for i,w in enumerate(words):
        print(i)
        curCount=binCount()
        config=pauseRead()
        
        idx=min(i+10,len(words))
        
        config["Positive_Prompt"]=''.join(filter(lambda x: x in printable, " ".join(words[i:idx])))
        
        config["From_Text"]=0
        if i==0:
            config["From_Text"]=1
            config["CFG_Scale"]=15
            
        if i==1:
            config["CFG_Scale"]=10
            
        config["Pause_Flag"]="0"
        
        with open("BRAIN.json","w") as outfile:
            outfile.write(json.dumps(config))
        if i==0:
            while(len([file for file in os.listdir("IO/IN")])==0):
                time.sleep(1)
        else:
            while curCount==binCount():
                time.sleep(0.5)
        
if __name__=='__main__':
    main()
