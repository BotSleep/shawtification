import cv2
import os
import numpy as np
import datetime
import os

cpath=str(os.path.abspath(os.getcwd())).replace("TO_VIDEO","IO\BIN\ ")
print(f"Null input defaults to {cpath}")
image_folder=str(input("Folder Path: "))
if image_folder=="":
    image_folder = '../IO/BIN/'
if image_folder[-1]+" " not in ['\ ','/ ']:
    image_folder +="/"
    
video_name = str(int(datetime.datetime.now().timestamp()))+'.mp4'
images = [f"{x}.png" for x in np.sort([int(file.split(".")[0]) for file in os.listdir(image_folder)])]
frame = cv2.imread(os.path.join(image_folder,images[0]))
height, width, layers = frame.shape

v= cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name,v, float(input("FPS: ")), (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()