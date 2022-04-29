#!/bin/sh

#blender

#open ~/Dev/BL/art-from-code
if [ $2 == "gif" ]; then
    mkdir -p ~/Dev/BL/art-from-code/output/temp_gif/
    cd ~/Dev/BL/art-from-code/output/temp_gif/
    rm -rf *.jpg
fi
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

#blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend --frame-start 2 --frame-end 1000 --frame-jump 249 --render-output //../output/temp_gif/
if [ $2 == "gif" ]; then
    /Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid-gif.py
fi
###############################################################################
#                                                                             #
###############################################################################


if [ $2 == "gif" ]; then
    open ~/Dev/BL/art-from-code/output/temp_gif/
    echo "GIF option enabled"
    cd ~/Dev/BL/art-from-code/output/temp_gif/
    convert -loop 0 -dispose previous *.jpg ./temp_grid$(date +"%m%d%y-%H%M").gif
    rm -rf *.jpg
else
    echo ""
    open ~/Dev/BL/art-from-code/output/
fi
