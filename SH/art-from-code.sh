#!/bin/sh

#blender

#open ~/Dev/BL/art-from-code

cd ~/Dev/BL/art-from-code

git pull https://github.com/erikhatfield/Art-from-Code.git

rm -rf ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend 
cp -a ~/Dev/BL/art-from-code/BL/grid.blend ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend

# make dir for text output if doesnt exist
mkdir -p ~/Dev/BL/art-from-code/output/temp_settings_txt/


#blender -b ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
# echo "alias blender=/Applications/Blender.app/Contents/MacOS/blender" >> ~/.bash_profile
#source ~/.bash_profile

# Without arguements (previous version)
#Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
# With arguements provided:
/Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py -- $1 $2 $3


###############################################################################
#                                                                             #
###############################################################################

open ~/Dev/BL/art-from-code/output
