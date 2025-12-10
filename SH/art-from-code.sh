#!/bin/bash

####################
#automated blender #
####################
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
relative_path=$(realpath "$0")
ART_FROM_CODE_DIRPATH=$(dirname $relative_path)"/.."

#ART_FROM_CODE_DIRPATH=~/Art/BL/art-from-code
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
######################################################################################
#blender version? 3 is good. ... blender 4 rearranged some material values so it hangs
eval $BLENDER_PATH -v

if [ "$2" == "gif" ]; then
    #gif parameter requires imagick ## consider revamping this option to be initiated AFTER (a steller) render, or as a standalone with .blend input
    mkdir -p $ART_FROM_CODE_DIRPATH/output/temp_gif/
    cd $ART_FROM_CODE_DIRPATH/output/temp_gif/
    rm -rfv *.jpg
fi
cd $ART_FROM_CODE_DIRPATH

###########################################################################
#check if command-line tools are setup (for git) otherwise skip git portion
if type xcode-select >&- && xpath=$( xcode-select --print-path ) &&
   test -d "${xpath}" && test -x "${xpath}" ; then
   git pull https://github.com/erikhatfield/Art-from-Code.git
else
   echo "command-line tools not installed, skipping % git"
fi
###########################################################################

# make dir for text output if doesnt exist
####mkdir -p $ART_FROM_CODE_DIRPATH/output/temp_settings_txt/

########################################################################
#remants of the past, sir. consider smurfing
#blender -b ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
# echo "alias blender=/Applications/Blender.app/Contents/MacOS/blender" >> ~/.bash_profile
#source ~/.bash_profile

# Without arguements (previous version)
#Applications/Blender.app/Contents/MacOS/blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend -P ~/Dev/BL/art-from-code/grid.py
########################################################################
# With arguements provided:

#blender ~/Dev/BL/art-from-code/BL/temp_auto_grid.blend --frame-start 2 --frame-end 1000 --frame-jump 249 --render-output //../output/temp_gif/
if [ "$2" == "gif" ]; then
    echo "using existing .blend for gif making:"
    echo "$ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend"
    #~/Applications/Blender.app/Contents/MacOS/blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid-gif.py
    ##blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid-gif.py
    eval $BLENDER_PATH $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid-gif.py
else
    rm -rf $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend
    cp -a $ART_FROM_CODE_DIRPATH/BL/grid.blend $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend
    #~/Applications/Blender.app/Contents/MacOS/blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid.py -- $1 $2 $3
    ##blender $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid.py -- $1 $2 $3
    eval $BLENDER_PATH $ART_FROM_CODE_DIRPATH/BL/temp_auto_grid.blend -P $ART_FROM_CODE_DIRPATH/grid.py -- $1 $2 $3
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
