#!/usr/bin/env python
#-*- coding:utf-8

import os
import os.path
import sys

button_width = 136
button_height = 128
icon_size = "84x84"

panel_settings = """
Style FvwmPanelDir !Title, !Handles, Borders, FixedPPosition, FixedSize
Style FvwmPanelDir !Iconifiable
Style FvwmPanelDir ParentalRelativity
Style FvwmPanelDir RoundedCorners
*FvwmPanelDir: ButtonGeometry %dx%d
*FvwmPanelDir: BoxSize smart
*FvwmPanelDir: Frame 0
*FvwmPanelDir: Padding 5 8
*FvwmPanelDir: Font "$[infostore.font_dirpanel]"
*FvwmPanelDir: Colorset 8
*FvwmPanelDir: ActiveColorset 2
*FvwmPanelDir: PressColorset 2
""" % (button_width, button_height)

def calculate_size(objs):
    rows = 1
    l = len(objs) + 1
    for i in range(1, 5, 1):
        rows = i
        if (rows+1) ** 2 > l:
            break
    columns = l / rows
    if l % rows != 0:
        columns += 1

    return rows, columns

def make_file_obj(p, x, y):
    suffix_icon_map = {
            ".xlsx" : "application-vnd.ms-excel",
            ".py"   : "text-x-python",
            ".exe"  : "gnome-mime-application-x-ms-dos-executable",
    }
    mime_icon_replace = {
            "application-x-bzip2" : "gnome-mime-application-x-bzip",
            "application-x-xz"    : "gnome-mime-application-x-bzip",
            "text-x-diff"         : "text-plain",
            "text-x-shellscript"  : "application-x-shellscript",
            "application-x-iso9660-image"  : "application-x-cd-image",
    }
    icon_name = None
    idx = p.rfind(".")
    if idx != -1:
        suffix = p[idx:]
        icon_name = suffix_icon_map.get(suffix, None)
    if not icon_name:
        with os.popen("file -b --mime-type '%s'" % p) as f:
            mime = f.read().strip()
            icon_name = mime.replace("/", "-")
            if mime_icon_replace.get(icon_name, None):
                icon_name = mime_icon_replace.get(icon_name, None)
    icon = "mimetypes/scalable/%s.svg:%s" % (icon_name, icon_size)
    print("*FvwmPanelDir: (Icon '%s', Title '%s', Action (Mouse 1) Exec xdg-open '%s' )" % (icon, os.path.basename(p), os.path.abspath(p)))

def make_folder_obj(p, x, y):
    folder_icons = {
            "music"     : "folder-music.svg",
            "Music"     : "folder-music.svg",
            "音乐"      : "folder-music.svg",
            "downloads" : "folder-downloads.svg",
            "Downloads" : "folder-downloads.svg",
            "下载"      : "folder-downloads.svg",
            "photos"    : "folder-pictures.svg",
            "Photos"    : "folder-pictures.svg",
            "照片"      : "folder-pictures.svg",
            "pictures"  : "folder-pictures.svg",
            "Pictures"  : "folder-pictures.svg",
            "图片"      : "folder-pictures.svg",
            "Documents" : "folder-documents.svg",
            "documents" : "folder-documents.svg",
            "文档"      : "folder-documents.svg",
            "Videos"    : "folder-videos.svg",
            "videos"    : "folder-videos.svg",
            "视频"      : "folder-videos.svg",
            "desktop"   : "user-desktop.svg",
            "Desktop"   : "user-desktop.svg",
            "桌面"      : "user-desktop.svg",
    }
    basename = os.path.basename(p)
    icon = folder_icons.get(basename, "folder.svg")
    action_stub = "(Mouse 1) Function ShowFvwmPanelDir '%s' %d %d"
    action = action_stub % (p, x, y)
    print("*FvwmPanelDir: (Icon 'places/scalable/%s:%s', Title '%s', Action %s)" % (icon, icon_size, basename, action))

def make_dir_panel(path, x=0, y=0):
    more2show = False
    objs = [os.path.join(path, "..")]
    for p in os.listdir(path):
        if p.startswith("."):
            continue
        objs.append(os.path.abspath(os.path.join(path,p)))
    if len(objs) > 25:
        objs = objs[:25]
        more2show = True
    print(panel_settings)
    rows, columns = calculate_size(objs)
    print("*FvwmPanelDir: Rows %d" % rows)
    width = columns * button_width
    height = rows * button_height
    geometry_str = ("*FvwmPanelDir: Geometry %dx%d+%d+%d" % (width, height, x-width/2, y-height-4))
    print(geometry_str)
    for p in objs:
        if os.path.isdir(p):
            make_folder_obj(p, x, y)
        else:
            make_file_obj(p, x, y)
    if more2show:
        print("*FvwmPanelDir: (Icon 'emblems/scalable/emblem-symbolic-link.svg:%s', Title '更多文件...', Action (Mouse 1) Exec xdg-open '%s')" % (icon_size, path))
    else:
        print("*FvwmPanelDir: (Icon 'emblems/scalable/emblem-symbolic-link.svg:%s', Title '打开文件夹', Action (Mouse 1) Exec xdg-open '%s')" % (icon_size, path))

if __name__ == "__main__":
    make_dir_panel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
