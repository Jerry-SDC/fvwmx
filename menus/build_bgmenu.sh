#!/usr/bin/env sh

bg_search_dirs="${HOME}/Pictures/ ${HOME}/Downloads ${HOME}/.fvwm/background/"
bg_search_exts=".jpg .png .jpeg"

for dir in ${bg_search_dirs}; do
    for ext in ${bg_search_exts}; do
        for f in `ls ${dir}/*${ext} 2> /dev/null`; do
            bgmenu_name=`basename ${f}`
            bgmenu_icon="${FVWM_TMPDIR}/bgmenu_${bgmenu_name}"
            if [ ! -f ${bgmenu_icon} ]; then
                convert ${f} -resize 96 -quality 0 png:${bgmenu_icon} &> /dev/null;
            fi;
            echo -n + %${bgmenu_icon}%\"${bgmenu_name}\";
            echo -n " "
            echo "SetBackground ${f}"
            #echo '+ "" Nop'
        done
    done
done
