# shawtification
{<br/>
"Positive_Prompt":"",<br/>
"Negative_Prompt":"",<br/>
"Dimension":512,<br/>
"CFG_Scale": 10,<br/>
"Denoise":0.5,<br/>
"Sampler_Index":2,<br/>
"Steps":35<br/>

The above are parameters that should be known.<br/>
Input a starting image in Shawtys_trinkets/io/in<br/>
That image should be square.<br/>
From that point, Run_gear can be ran and the iterative process will begin with these paramaters.<br/>

For Z_pixels, these are the border pixels of the image that are either taken or added.<br/>
  [zoom in] EG: -1 a 100x100 has a pixel border removed such that its 98x98, and then is resized<br/>
  [zoom out] EG: 1 a 100x100 is resized to 98x98 and placed on top of the original 100<br/>

M_pixels: Intended to only be used with z_pixels.<br/>
        Any value greater than 0 masks the entire image, except a frame of # pixels.<br/>
        so a 100x100 image, given a 1 m_pixels, means the center 98x98 pixels are blocked from being edited.<br/>
        In conjunction with zooming out, this is beneficial.<br/>

Pause flag: Switch to anything other than "0" and itll pause at the next step,<br/>
useful for switching out source images without having to restart the process.<br/>

"Z_Pixels":3,<br/>
"M_Pixels":10,<br/>
"M_Blur":5,<br/>
"Pause_Flag":"0"<br/>
}<br/>
