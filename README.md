
## Parameters
### Zoom:
Z_Pixels: Zoom direction [In,Out] and magnitude
- [ Z_Pixels > 0 = Zoom Out] The image is sized down, and placed within itself. 
	- EG: a 100x100 image with Z_pixels 1, is resized to 98x98. 98x98 is centered on top of 100x100.
- [ Z_Pixels > 0 = Zoom Out] The image is simply cropped and resized. 
	- EG: (100x100 take inner 98x98, resize to 100x100).

Z_Lean: Zoom Direction [Left Right Up Down None]
- This parameter requires Z_pixels !=0. 
	- For a Z_Pixel=1 and Z_Lean=U:
		- The 100x100 image is resized to 98x98. 98x98 is horizontally centered, but vertically touched the top border. Carry this example through the other directions, and the inverse of Z_pixels=-1
		
M_Pixels: A inverse Mask to be applied when using Zoom.
- M_Pixels can only be a positive value. It is the amount of pixels around the image to actually edit. Essentially, Z_pixels=5 means there is a border of 5 pixels on every side that are 'new'. W/ M_Pixels=5, The only editable pixels are that border. 

### Color Correction
Color_Correct: 
- Value of 1 causes output to be color corrected. This correction requires a reference image. That reference image should likely be the initial source image of a iteration, rename as "CC_SOURCE.png" and placed in SHAWTYS_TRINKETS/IO/TMP/

### Pause_Flag
- Setting this flag to any value other than "0" causes the gear process to stop/pause on the next step. This way you can switch out the source/ IN image, without having to restart the gear process.

## Programs
### SHOW
 - Shows the last output in a running iteration, optionally animates through all the produced images.
### MAKE VIDEO
 - Compile a input: folder into a mp4 with input: FPS
### BIN OUT
 - Toss the current bin folder of images into BinOut, quick cleanup
### STORYMODE
 - Dynamically edits the BRAIN.json file while the gear process is running. It runs through the given script.txt, and can additionally alter other parameters at each step. Currently creates the initial image with txt2img, before feeding it in to run with img2img for the duration. Has potential, not much there currently.

