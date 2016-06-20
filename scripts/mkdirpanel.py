#!/usr/bin/env python

import os
import os.path
import sys

button_width = 128
button_height = 156
icon_size = 96

panel_settings = """
Style FvwmPanelDir !Title, !Handles, Borders, FixedPPosition, FixedSize
Style FvwmPanelDir !Iconifiable
Style FvwmPanelDir ParentalRelativity
Style FvwmPanelDir RoundedCorners
*FvwmPanelDir: ButtonGeometry %dx%d
*FvwmPanelDir: BoxSize smart
*FvwmPanelDir: Frame 0
*FvwmPanelDir: Padding 5 8
*FvwmPanelDir: Font "$[FVWM_BOLD_FONT]"
*FvwmPanelDir: Colorset 8
*FvwmPanelDir: ActiveColorset 2
*FvwmPanelDir: PressColorset 2
""" % (button_width, button_height)

def calculate_size(objs):
    rows = 1
    l = len(objs) + 1
    for i in range(1, 6, 1):
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
    }
    icon_name = None
    idx = p.rfind(".")
    if idx != -1:
        suffix = p[idx:]
        icon_name = suffix_icon_map.get(suffix, None)
    if not icon_name:
        """
        with os.popen("xdg-mime query filetype %s" % p) as f:
            icon_name = f.read().strip().replace("/", "-")
        """
        with os.popen("file --mime-type %s" % p) as f:
            name, mime = f.read().split(":")
            icon_name = mime.strip().replace("/", "-")
            if mime_icon_replace.get(icon_name, None):
                icon_name = mime_icon_replace.get(icon_name, None)
    icon = "mimetypes/%d/%s.png" % (icon_size, icon_name)
    print("*FvwmPanelDir: (Icon '%s', Title '%s', Action (Mouse 1) Exec xdg-open '%s' )" % (icon, os.path.basename(p), os.path.abspath(p)))

def make_folder_obj(p, x, y):
    folder_icon_map = {
            "music"     : "folder-music.png",
            "Music"     : "folder-music.png",
            "音乐"      : "folder-music.png",
            "downloads" : "folder-downloads.png",
            "Downloads" : "folder-downloads.png",
            "下载"      : "folder-downloads.png",
            "photos"    : "folder-pictures.png",
            "Photos"    : "folder-pictures.png",
            "照片"      : "folder-pictures.png",
            "pictures"  : "folder-pictures.png",
            "Pictures"  : "folder-pictures.png",
            "图片"      : "folder-pictures.png",
            "Documents" : "folder-documents.png",
            "documents" : "folder-documents.png",
            "文档"      : "folder-documents.png",
            "Videos"    : "folder-videos.png",
            "videos"    : "folder-videos.png",
            "视频"      : "folder-videos.png",
            "desktop"   : "user-desktop.png",
            "Desktop"   : "user-desktop.png",
            "桌面"      : "user-desktop.png",
    }
    basename = os.path.basename(p)
    icon = folder_icon_map.get(basename, "folder.png")
    action_stub = "(Mouse 1) Function ShowFvwmPanelDir %s %d %d"
    action = action_stub % (os.path.abspath(p), x, y)
    print("*FvwmPanelDir: (Icon 'places/%d/%s', Title '%s', Action %s)" % (icon_size, icon, basename, action))

def make_dir_panel(path, x=0, y=0):
    objs = []
    for p in os.listdir(path):
        if p.startswith("."):
            continue
        objs.append(os.path.join(path,p))
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
    print("*FvwmPanelDir: (Icon 'emblems/scalable/emblem-symbolic-link.svg:%dx%d', title '打开文件夹...', Action (Mouse 1) Exec xdg-open '%s')" % (icon_size, icon_size, path))

if __name__ == "__main__":
    make_dir_panel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
