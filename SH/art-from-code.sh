#!/bin/sh

####################
#automated blender #
####################
ART_FROM_CODE_DIRPATH=~/Art/BL/art-from-code

if [ "$2" == "gif" ]; then
    #gif parameter requires imagick ## consider revamping this option to be initiated AFTER (a steller) render, or as a standalone with .blend input 
    mkdir -p $ART_FROM_CODE_DIRPATH/output/temp_gif/
    cd $ART_FROM_CODE_DIRPATH/output/temp_gif/
    rm -rfv *.jpg
fi
cd $ART_FROM_CODE_DIRPATH

git pull https://github.com/erikhatfield/Art-from-Code.git

rm -rf $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend 
cp -a $ART_FROM_CODE_DIRPATH/BL/grid.blend $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend

# make dir for text output if doesnt exist
mkdir -p $ART_FROM_CODE_DIRPATH/output/temp_settings_txt/

########################################################################
#remants of the past, sir. consider smurfing
#blender -b ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
# echo "alias blender=/Applications/Blender.app/Contents/MacOS/blender" >> ~/.bash_profile
#source ~/.bash_profile

# Without arguements (previous version)
#Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
########################################################################
# With arguements provided:
#~/Applications/Blender.app/Contents/MacOS/blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid.py -- $1 $2 $3
blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid.py -- $1 $2 $3

#blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend --frame-start 2 --frame-end 1000 --frame-jump 249 --render-output //../output/temp_gif/
if [ "$2" == "gif" ]; then
    #~/Applications/Blender.app/Contents/MacOS/blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid-gif.py
    blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid-gif.py
fi


###############################################################################
# SEMI INTENTIONAL EMPTY HASH BOX THIS IS                                     #
###############################################################################


if [ "$2" == "gif" ]; then
    open $ART_FROM_CODE_DIRPATH/output/temp_gif/
    echo "GIF option enabled"
    cd $ART_FROM_CODE_DIRPATH/output/temp_gif/
    convert -loop 0 -dispose previous *.jpg ./temp_grid$(date +"%m%d%y-%H%M").gif
    rm -rf *.jpg
else
    echo ""
    #open $ART_FROM_CODE_DIRPATH/output/
fi
