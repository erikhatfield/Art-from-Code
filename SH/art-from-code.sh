#!/bin/sh

#blender

#open ~/Dev/BL/art-from-code

cd ~/Dev/BL/art-from-code

git pull https://github.com/erikhatfield/Art-from-Code.git

rm -rf ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend 
cp -a ~/Dev/BL/art-from-code/BL/grid.blend ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend

#blender -b ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
# echo "alias blender=/Applications/Blender.app/Contents/MacOS/blender" >> ~/.bash_profile
#source ~/.bash_profile
/Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py


###############################################################################
#                                                                             #
###############################################################################

open ~/Dev/BL/art-from-code/output
