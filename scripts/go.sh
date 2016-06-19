#!/usr/bin/env bash

more_apps=1

apps=""
# Basic Packages
apps+=" xorg xorg-xinit xterm rxvt-unicode"
# Themes and Fonts
apps+=" gnome-themes-standard faenza-icon-theme"
apps+=" adobe-source-han-sans-cn-fonts ttf-fira-mono ttf-fira-sans"
apps+=" lxappearance"
# Utilities
apps+=" conky imagemagick stalonetray scrot"
apps+=" surf st"
apps+=" fcitx-im"
# Applet
apps+=" volumeicon"

# optional Apps
if [ x$more_apps == x1 ]; then
    apps+=" base-devel git"
    apps+=" vim ctags"
    apps+=" chromium"
    apps+=" networkmanager network-manager-applet"
fi

sudo pacman -S --noconfirm --needed $apps

XINITRC=${HOME}/.xinitrc
echo export LANG=zh_CN.UTF-8 > ${XINITRC}
echo export LC_ALL=zh_CN.UTF-8 >> ${XINITRC}
echo fvwm >> ${XINITRC}
