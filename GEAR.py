import modules.processing as proc
import modules.sd_models as sd
import modules.shared as sh
from PIL import Image
import numpy as np
import datetime
import time
import json
import cv2
import os

def grabJson():
    global pause_flag

    config=json.load(open("SHAWTYS_TRINKETS/BRAIN.json"))

    
    
    storeParams={
        "prompt":                      str(config["Positive_Prompt"]),
        "cfg_scale":                   float(config["CFG_Scale"]),
        "sampler_index":          int(config["Sampler_Index"]),
        "steps":                          int(config["Steps"]),
        "width":                         int(config["Dimension"]),
        "height":                        int(config["Dimension"]),
        "denoising_strength":   float(config["Denoise"])
    }
    
    if str(config["Pause_Flag"])!="0":
        pause_flag=1
        return storeParams.update(defaulted_args)
    else:
        pause_flag=0
        
    zint=int(config["Z_Pixels"])
    img=cv2.imread(source_dir+[file for file in os.listdir(source_dir)][0])
    
    if zint==0:
        storeParams["init_images"]=[img]
    else:
        dims=img.shape[0:2]
        
        if zint>0:
            img[zint:dims[0]-zint,zint:dims[1]-zint,:]=cv2.resize(img, (dims[0]-zint*2,dims[0]-zint*2), interpolation = cv2.INTER_AREA)
        else:
            zint=abs(zint)
            img = cv2.resize(img[zint:dims[0]-zint,zint:dims[1]-zint,:], dims, interpolation = cv2.INTER_AREA)
            
        try:
            os.remove(Z_file)
        except:
            pass
        
        cv2.imwrite(Z_file,img)
        storeParams["init_images"]=[(Image.open(Z_file)).convert("RGBA")]

    if config["M_Pixels"]>0:
        try:
            os.remove(M_file)
        except:
            pass
        M=int(config["M_Pixels"])
        block=np.zeros((img.shape[0]-M*2,img.shape[1]-M*2,3))
        noblock=np.ones((img.shape[0],img.shape[0],3))
        noblock[M:img.shape[0]-M,M:img.shape[1]-M,:]=block
        cv2.imwrite(M_file,(noblock*255).astype(np.uint8))
        mask=Image.open(M_file)
        mask=mask.convert("RGBA")
        mData=mask.getdata()
        nData=[]
        for i in mData:
            if i[0:3]==(0,0,0):
                nData.append((0,0,0,0))
            else:
                nData.append(i)
        mask.putdata(nData)
        storeParams["mask"]=mask
        storeParams["mask_blur"]=int(config["M_Blur"])

    
    storeParams.update(defaulted_args)

    return storeParams

def automate():
    while True:
        '''
        Rebooting this specific program requires the initialization of a venv.
        To prevent the need for a restart after a cycles been initiated
        setting the Brain.json pause flag to anythin other than "0" pauses the cycle.
        This would allow you to replace the starting image, without needing to restart.
        '''
        params=grabJson()
        while pause_flag!=0:
            params=grabJson()
            time.sleep(1)
            print("Paused....",end='\r')
        print('\n')
        #using paramaters obtained from BRAIN.json, run with the image in /IN dir
        proc.process_images(proc.StableDiffusionProcessingImg2Img(**dict(params)))
        
        #take the /IN dir image, move it to bin. Start naming at 0.png, and increment
        safeName=np.max([int(file.split(".")[0]) for file in os.listdir(store_dir)]+[-1])+1
        os.rename(source_dir+[file for file in os.listdir(source_dir)][0],f"{store_dir}{safeName}.png")
        
        #take the image just produced, move it to /IN dir
        output_img=[file for file in os.listdir(output_dir)][0]
        os.rename(output_dir+ output_img, source_dir+ output_img)
        
        
        
        
        
    return
        
if __name__=='__main__':
    
    source_dir="SHAWTYS_TRINKETS/IO/IN/"
    output_dir="SHAWTYS_TRINKETS/IO/OUT/"
    store_dir="SHAWTYS_TRINKETS/IO/BIN/"
    Z_file="SHAWTYS_TRINKETS/IO/Z_FILE/Z_SOURCE.png"
    M_file="SHAWTYS_TRINKETS/IO/Z_FILE/M_SOURCE.png"
    
    #Move current BIN files to BIN_OUT
    if len([file for file in os.listdir(store_dir)])!=0:
        folder_name=f"SHAWTYS_TRINKETS/BIN_OUT/{int(datetime.datetime.now().timestamp())}/"
        os.makedirs(folder_name)
        for file in os.listdir(store_dir):
            os.rename(store_dir+file,folder_name+file)
    
    if len([file for file in os.listdir(source_dir)])==0:
        print("\nThere is currently no source file in SHAWTYS_TRINKETS/IO/IN/ \n",
                    "Please place your starting image there. \n",
                    "Ensure the image is square [else it will be resized, not cropped.] \n",
                   "Configure SHAWTYS_TRINKETS\BRAIN.json with desired parameters \n",
                  "\t \t \t Note on Parameters: \n",
                  "\t All parameters can be edited while this program runs. \n",
                  "\t They will take effect on the next iteration. Make sure to ctrl+s. \n",
                "\t Z_Pixels: number of pixels around the image to add or remove. + zooms out, - in. 0 nothing. \n",
                "\n \t Pause_Flag: setting this to any value besides '0' will pause on the next load. \n",
                "\n \t \t \t This helps switch out source files without having to restart the program \n")
        print("\nWhen finished press any key to begin.")
        input("Waiting...")
    
    SDV14=sd.load_model()
    sh.sd_model=SDV14
    
    defaulted_args ={
        "sd_model":SDV14, 
        "outpath_samples":output_dir,
        "outpath_grids":output_dir,
        "styles":"Just Resize", 
        "restore_faces":False  
    }
    
    pause_flag=1
    automate()