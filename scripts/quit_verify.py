#!/usr/bin/env python

import sys, os
from gi.repository import Gtk

def do_response(widget, data):
    if data == 1:
        os.system("FvwmCommand Restart")
    elif data == 2:
        os.system("FvwmCommand Quit")
    elif data == 3:
        os.system("sudo reboot")
    elif data == 4:
        os.system("sudo poweroff")
    else:
        pass
    Gtk.main_quit()

Gtk.init(sys.argv)

win = Gtk.Dialog("Quit FVWM?", None)
win.connect("delete-event", Gtk.main_quit)
msg = Gtk.Label("Do you really want to quit?")
c = win.get_content_area()
c.pack_start(msg, True, True, 5)
win.add_button("Logout", 2)
win.add_button("Reboot", 3)
win.add_button("Power Off", 4)
win.connect("response", do_response)
win.show_all()

Gtk.main()
