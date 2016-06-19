#!/usr/bin/env sh

background_dir="${HOME}/Pictures/ ${HOME}/Downloads ${HOME}/.fvwm/background/"
background_ext=".jpg .png .jpeg"

for dir in ${background_dir}; do
    for ext in ${background_ext}; do
        for f in `ls ${dir}/*${ext} 2> /dev/null`; do
            bg_name=`basename ${f}`
            convert ${f} -resize 96 -quality 0 png:/tmp/bgmenu_${bg_name} &> /dev/null;
            echo -n + %/tmp/bgmenu_${bg_name}%\"${bg_name}\";
            echo -n " "
            echo "SetBackground ${f}"
            #echo '+ "" Nop'
        done
    done
done
