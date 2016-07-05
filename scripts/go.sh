#!/usr/bin/env bash

developement_tools=1

apps=""
# Xorg Packages
apps+=" xorg xorg-xinit xterm"
# Session Manager
apps+=" lightdm lightdm-gtk-greeter"
# Themes and Fonts
apps+=" gnome-themes-standard faenza-icon-theme"
apps+=" adobe-source-han-sans-cn-fonts ttf-fira-mono ttf-fira-sans"
# Utilities
apps+=" conky imagemagick stalonetray scrot"
# Applet
apps+=" fcitx-im"
apps+=" volumeicon"
apps+=" networkmanager network-manager-applet"

# optional Apps
if [ x$developement_tools == x1 ]; then
    apps+=" base-devel git"
    apps+=" vim ctags"
fi

# Applications
apps+=" gpicview"     # Picture/Photo View
apps+=" nautilus"     # File Manager
apps+=" epiphany"     # Browser
apps+=" lxappearance" # Theme/Font configuration
apps+=" surf st dmenu"

sudo pacman -S --noconfirm --needed $apps

sudo systemctl enable NetworkManager
sudo systemctl enable lightdm

XINITRC=${HOME}/.xinitrc
echo export LANG=zh_CN.UTF-8 > ${XINITRC}
echo export LC_ALL=zh_CN.UTF-8 >> ${XINITRC}
echo fvwm >> ${XINITRC}
