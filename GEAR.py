import modules.processing as proc
import modules.sd_models as sd
import modules.shared as sh

from skimage import exposure
from PIL import Image
import numpy as np
import datetime
import shutil
import time
import json
import cv2
import os

check=["SHAWTYS_TRINKETS/BIN_OUT/","SHAWTYS_TRINKETS/IO/OUT/","SHAWTYS_TRINKETS/IO/IN/","SHAWTYS_TRINKETS/IO/BIN/"]
for i in range(4):
    try:
        os.remove(check[i]+".gitkeep")
    except:
        pass
    


def grabJson():
    global pause_flag,textMode,cc_correct

    config=json.load(open("SHAWTYS_TRINKETS/BRAIN.json"))

    storeParams={
        "prompt":                      str(config["Positive_Prompt"]),
        "negative_prompt":      str(config["Negative_Prompt"]),
        "cfg_scale":                   float(config["CFG_Scale"]),
        "sampler_index":          int(config["Sampler_Index"]),
        "steps":                          int(config["Steps"]),
        "width":                         int(config["Dimension"]),
        "height":                        int(config["Dimension"])
    }
    
    if str(config["Pause_Flag"])!="0":
        pause_flag=1
        return storeParams.update(defaulted_args)
    else:
        pause_flag=0
    
    if int(config["From_Text"])!=0:
        textMode=1
        return storeParams
    else:
        textMode=0
    
    cc_correct=0
    if int(config["Color_Correct"])==1:
        cc_correct=1
        if not (os.path.exists(C_file)):
            try:
                cc=cv2.imread(source_dir+[file for file in os.listdir(source_dir)][0])
                cc=cv2.resize(cc,(int(storeParams["height"]),int(storeParams["height"])),cv2.INTER_AREA)
                cv2.imwrite("SHAWTYS_TRINKETS/IO/TMP/CC_SOURCE.png",cc)
            except:
                print("Couldn't create color_correction source file. Place file in IO/TMP/ named 'CC_SOURCE.png'")

        
    storeParams["denoising_strength"]=float(config["Denoise"])
    
    zint=int(config["Z_Pixels"])
    
    img=Image.open(source_dir+[file for file in os.listdir(source_dir)][0])
    if img.size[0]!=storeParams["width"] or img.size[1]!=storeParams["width"]:
        img=img.resize((storeParams["width"],storeParams["width"]),2)
        img.save(source_dir+[file for file in os.listdir(source_dir)][0])
    
    if zint==0:
        storeParams["init_images"]=[img]
        
    else:
        img=cv2.imread(source_dir+[file for file in os.listdir(source_dir)][0])
        dims=img.shape[0:2]
        
        z=abs(zint)
        Lean=str(config["Z_Lean"])
        LY=z
        UY=dims[0]-z
        LX=z
        UX=dims[0]-z
        
        if  Lean=="D" or Lean=="U":
            LX=z
            UX=dims[0]-z
            LY=0
            UY=dims[0]-2*z
            if Lean=="D":
                LY=2*z
                UY=dims[0]

        elif  Lean=="L" or Lean=="R":
            LY=z
            UY=dims[0]-z
            LX=z*2
            UX=dims[0]
            if Lean=="L":
                LX=0
                UX=dims[0]-z*2
            
        if zint>0:
            img[LY:UY,LX:UX,:]=cv2.resize(img, (dims[0]-zint*2,dims[0]-zint*2), interpolation = cv2.INTER_AREA)
        else:
            img = cv2.resize(img[LY:UY,LX:UX,:], dims, interpolation = cv2.INTER_AREA)
            
        try:
            os.remove(Z_file)
        except:
            pass
        
        cv2.imwrite(Z_file,img)
        storeParams["init_images"]=[(Image.open(Z_file)).convert("RGBA")]
    ss=(storeParams["init_images"][0]).size[0]
    if int(config["M_Pixels"])>0:
        try:
            os.remove(M_file)
        except:
            pass
        M=int(config["M_Pixels"])
        block=np.zeros((ss-M*2,ss-M*2,3))
        noblock=np.ones((ss,ss,3))
        noblock[M:ss-M,M:ss-M,:]=block
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
        mask.save(M_file)
        storeParams["mask"]=mask
        storeParams["mask_blur"]=int(config["M_Blur"])

    return storeParams

def automate():
    while True:
        
        params=grabJson()
        while pause_flag!=0:
            params=grabJson()
            time.sleep(1)
            print("Paused....",end='\r')
        print([str(x)+str(params[x])+"\n"  for x in params if x!= "init_images"])
        params.update(defaulted_args)
        
        if textMode==0:
            #using paramaters obtained from BRAIN.json, run with the image in /IN dir
            proc.process_images(proc.StableDiffusionProcessingImg2Img(**dict(params)))
            
            #take the /IN dir image, move it to bin. Start naming at 0.png, and increment
            safeName=np.max([int(file.split(".")[0]) for file in os.listdir(store_dir)]+[-1])+1
            os.rename(source_dir+[file for file in os.listdir(source_dir)][0],f"{store_dir}{safeName}.png")
        
        if textMode==1:
            proc.process_images(proc.StableDiffusionProcessingTxt2Img(**dict(params)))
            try:
                safeName=np.max([int(file.split(".")[0]) for file in os.listdir(store_dir)]+[-1])+1
                os.rename(source_dir+[file for file in os.listdir(source_dir)][0],f"{store_dir}{safeName}.png")
            except:
                pass
                
        #take the image just produced, move it to /IN dir
        output_img=[file for file in os.listdir(output_dir)][0]
        if cc_correct==1 and os.path.exists(Z_file):
            print("CCING")
            Image.fromarray(exposure.match_histograms(
                    cv2.cvtColor(np.asarray(Image.open(output_dir+output_img)),cv2.COLOR_RGB2RGBA),
                    cv2.cvtColor(cv2.imread(C_file),cv2.COLOR_BGR2RGBA),
                    channel_axis=2).astype("uint8")).save(source_dir+output_img)
            os.remove(output_dir+output_img)
        else:
            os.rename(output_dir+ output_img, source_dir+ output_img)
        if textMode==1:
            time.sleep(2)
    return
        
if __name__=='__main__':
    
    source_dir="SHAWTYS_TRINKETS/IO/IN/"
    output_dir="SHAWTYS_TRINKETS/IO/OUT/"
    store_dir="SHAWTYS_TRINKETS/IO/BIN/"
    Z_file="SHAWTYS_TRINKETS/IO/TMP/Z_SOURCE.png"
    M_file="SHAWTYS_TRINKETS/IO/TMP/M_SOURCE.png"
    C_file="SHAWTYS_TRINKETS/IO/TMP/CC_SOURCE.png"
    
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
    
    pause_flag,textMode,cc_correct=1,0,0
    automate()