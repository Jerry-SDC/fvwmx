#!/usr/bin/env python
#-*- coding:utf-8

import os
import os.path
import sys

button_width = 96
button_height = 75
icon_size = 36

UnusedPaths = (
        )

AppIconPaths = (
        "/usr/share/icons/Faenza/apps/scalable/",
        "/usr/share/icons/Faenza/categories/scalable/",
        "/usr/share/icons/Faenza/devices/scalable/",
        "/usr/share/icons/Faenza/status/scalable/",
        "/usr/share/icons/Faenza/actions/scalable/",
        "/usr/share/icons/Adwaita/scalable/apps/",
        "/usr/share/icons/Adwaita/scalable/categories/",
        "/usr/share/icons/hicolor/scalable/apps/",
        "/usr/share/icons/hicolor/48x48/apps/",
        "/usr/share/icons/hicolor/32x32/apps/",
        "/")

panel_settings = """
Style FvwmPanelApp !Title, !Handles, Borders, FixedPPosition, FixedSize
Style FvwmPanelApp !Iconifiable
Style FvwmPanelApp ParentalRelativity
Style FvwmPanelApp RoundedCorners
*FvwmPanelApp: ButtonGeometry %dx%d
*FvwmPanelApp: BoxSize smart
*FvwmPanelApp: Frame 0
*FvwmPanelApp: Padding 5 8
*FvwmPanelApp: Font "$[infostore.font_appgrid]"
*FvwmPanelApp: Colorset 9
*FvwmPanelApp: ActiveColorset 2
*FvwmPanelApp: PressColorset 2
""" % (button_width, button_height)

def calculate_size(objs):
    rows = 1
    l = len(objs) + 1
    for i in range(1, 11, 1):
        rows = i
        if (rows+1) ** 2 > l:
            break
    columns = l / rows
    if l % rows != 0:
        columns += 1

    return rows, columns

def make_app_obj(app, x, y):
    if app.get("NoDisplay", None):
        return
    #
    # get app name
    # 
    name = app.get("Name[zh_CN]", None)
    if not name:
        name = app.get("Name", None)
    if not name:
        name = app.get("Debug")
    #
    # get app icon
    #
    icon_name = app.get("Icon", "application-default-icon")
    icon = "application-default-icon.svg:%dx%d" % (icon_size, icon_size)
    path = os.path.basename(app.get("Path", "Unknow"))
    for path in AppIconPaths:
        fullpath = os.path.join(path, icon_name)
        svg_path = "%s.svg" % fullpath
        if os.path.exists(svg_path):
            icon = "%s:%dx%d" % (svg_path, icon_size, icon_size)
            break
        png_path = "%s.png" % fullpath
        if os.path.exists(png_path):
            icon = "%s" % png_path
            break
        if os.path.exists(fullpath):
            icon = fullpath
    #
    # get app action
    #
    command = app.get("Exec", "Nop").split()
    action = "(Mouse 1) Exec %s" % command[0]
    print("*FvwmPanelApp: (icon '%s', title '%s', action %s)" % (icon, name, action))

def parse_desktop_file(path):
    entry = {"Debug": os.path.basename(path)}
    with open(path, "r") as f:
        desktop_entry = False
        for line in f:
            if line.startswith("["):
                if line.startswith("[Desktop Entry]"):
                    desktop_entry = True
                else:
                    desktop_entry = False
            if not desktop_entry:
                continue
            if len(line.split("=")) == 2:
                t, v = line.split("=")
                entry[t] = v.strip()
    return entry

def make_app_panel(path, x=0, y=0):
    objs = []
    for p in os.listdir(path):
        if not p.endswith(".desktop"):
            continue
        objs.append(parse_desktop_file(os.path.join(path,p)))
    print(panel_settings)
    rows, columns = calculate_size(objs)
    print("*FvwmPanelApp: Rows %d" % rows)
    width = columns * button_width
    height = rows * button_height
    geometry_str = ("*FvwmPanelApp: Geometry %dx%d+%d+%d" % (width, height, x, y-height-4))
    print(geometry_str)
    for app in objs:
        make_app_obj(app, x, y)

if __name__ == "__main__":
    make_app_panel(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
