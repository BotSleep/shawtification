import os
import cv2
import time
import numpy as np

def showLatest(files):
    print(f"BIN/{np.max(files)}.png")
    latest=cv2.imread(f"BIN/{np.max(files)}.png")
    latest=cv2.resize(latest,(512,512), interpolation = cv2.INTER_AREA)
    cv2.imshow("Latest",latest)
    cv2.waitKey(100)
    print(np.max(files),end='\r')

if __name__=="__main__":
    a,b=0,0
    saved=[]
    mov=[]
    sho=str(input("Animate? [Y/N]:"))
    while True:
        files=np.sort([int(file.split(".")[0]) for file in os.listdir("BIN")])
        try:
            showLatest(files)
        except:
            print("Latest /BIN image not found",end='/r')
        
        if sho!="N" and sho!="n":
            for i,v in enumerate(files):
                if v not in saved:
                    cur=cv2.resize(cv2.imread(f"bin/{v}.png"),(512,512), interpolation = cv2.INTER_AREA)
                    mov.append(cur)
                    saved.append(v)
                cv2.imshow("All",mov[i])
                cv2.waitKey(100)
            time.sleep(0.1)
        