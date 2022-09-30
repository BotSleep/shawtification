# shawtification
{
"Positive_Prompt":"",
"Negative_Prompt":"",
"Dimension":512,
"CFG_Scale": 10,
"Denoise":0.5,
"Sampler_Index":2,
"Steps":35

The above are parameters that should be known.
Input a starting image in Shawtys_trinkets/io/in
That image should be square.
From that point, Run_gear can be ran and the iterative process will begin with these paramaters.

For Z_pixels, these are the border pixels of the image that are either taken or added.
  [zoom in] EG: -1 a 100x100 has a pixel border removed such that its 98x98, and then is resized
  [zoom out] EG: 1 a 100x100 is resized to 98x98 and placed on top of the original 100

M_pixels: Intended to only be used with z_pixels.
        Any value greater than 0 masks the entire image, except a frame of # pixels.
        so a 100x100 image, given a 1 m_pixels, means the center 98x98 pixels are blocked from being edited.
        In conjunction with zooming out, this is beneficial.

Pause flag: Switch to anything other than "0" and itll pause at the next step, useful for switching out source images without 
having to restart the process.

"Z_Pixels":3,
"M_Pixels":10,
"M_Blur":5,
"Pause_Flag":"0"
}
