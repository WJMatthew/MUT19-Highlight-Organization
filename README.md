# MUT19 Highlight Organization
### Matthew Johnson, 2019

I started this project because I had 89Gb worth of 1 minute video clips containing highlights (~2100 clips) taken from Madden 19. Most of which were from a mode called squads (2v2 or 3v3). I wanted to organize these by play type without manually watching all of them. 

I was already (usually) saving the screenshot at a time where the play art was still visible [IMG HERE]. 

I began by extracting the final frame of each  video as an image. From here I divided cropping the screencap into top and bottom. Top would tell us whether it was a squads match or not, where the bottom would tell us the play side (home and away matches switch side of play art) and what type of play it was (pass, run, or fake FG). 
[IMGs HERE]

[Distribution of labeled data IMG]

We could further divide this into other classifications:

Idea A
* Green TOUCHDOWN
* Green INT
* Other
Idea B
* Offense
* Defense 
Idea C
* Can we clip offensive play videos to previous play art call?

Goal: given a folder (89Gb) of .mp4 files divide them into folders based on play type (pass, run, fake fg) and match type (squads/ not-squads). 


CV2 was used for video and image handling and extraction where Pytorch was used for modeling.

Shutil to move files 

TODO A
* Implement way to not have multiple csvs every where. 
* Package up code better 

