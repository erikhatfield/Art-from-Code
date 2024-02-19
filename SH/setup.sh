#!/bin/bash

#########################################
#setup ~/Art dir and art cmd-line alias #
#########################################
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
relative_path=$(realpath "$0")
INIT_SETUP_PATH=$(dirname $relative_path)"/../.."
cd $INIT_SETUP_PATH
INIT_SETUP_PATH=$(pwd)
echo "INIT_SETUP_PATH="$INIT_SETUP_PATH

#store username in variable for dynamicness. $id -un <=> $whoami
whoamilol="$(id -un)"
#who am i | awk '{print $1}' #works with sudo
who_i_is=$(who am i | awk '{print $1}')
home_path="$HOME"
################
ART_DIR_PATH=$home_path"/Art/BL/art-from-code"
################
if [ ! -d $ART_DIR_PATH ];
	then
	    echo "Setting up art-from-code @ $ART_DIR_PATH"
      mkdir -p $ART_DIR_PATH
      cp -a $INIT_SETUP_PATH"/art-from-code/*" $INIT_SETUP_PATH"/art-from-code/.*" $ART_DIR_PATH

	else
    echo "The art-from-code dir already exists @ $ART_DIR_PATH"
    ls -ale $ART_DIR_PATH

fi
################
################

####################
BASH_PROFILE_PATH=$home_path"/.bash_profile"
ifEmptyNoMatch=$(cat $BASH_PROFILE_PATH | grep 'alias art="~/Art/BL/art-from-code')
if [ ! -z "$ifEmptyNoMatch" ]; then
	  echo "art alias ✓ already installed in $BASH_PROFILE_PATH"
else
		echo "Setting up art alias in $BASH_PROFILE_PATH"
    echo 'alias art="~/Art/BL/art-from-code/SH/art-from-code.sh"' >> $BASH_PROFILE_PATH
    #echo 'alias art="~/Art/BL/art-from-code/SH/art-from-code.sh"' >> ~/.zshrc

    # and then source both of them (so that it may work again within future terminal wins)
    source ~/.bash_profile
    #source ~/.zshrc

    echo 'test it with alias => art'
fi;
