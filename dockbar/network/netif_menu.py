#!/usr/bin/env python

import os,sys
import os.path

net_class_dir = "/sys/class/net/"

class NetIf:
    def __init__(self, ifname):
        self.name = ifname
        self.path = os.path.join(net_class_dir, ifname)

    def get_desc(self):
        vendor = None
        device = None

        vendor_path = os.path.join(self.path, "device", "vendor")
        if os.path.exists(vendor_path):
            f = open(vendor_path)
            vendor = f.read().strip()
        device_path = os.path.join(self.path, "device", "device")
        if os.path.exists(device_path):
            f = open(device_path)
            device = f.read().strip()

        if vendor and device:
            return "%s" % (self._get_devname_by_id(vendor, device))
        else:
            return "%s (%s)" % ("Unknow Device Vendor", self.name)

    def carrier_on(self):
        with open(os.path.join(self.path, "carrier"), "r") as f:
            carrier = f.read().strip()
            if carrier == "1":
                return True
            else:
                return False

    def _get_devname_by_id(self, vendor, device):
        db = "/usr/share/hwdata/pci.ids"
        with open(db, "r") as f:
            line = f.readline()
            while line:
                if not line.startswith(vendor[2:]):
                    line = f.readline()
                    continue
                line = f.readline()
                while line:
                    if line.startswith("#"):
                        line = f.readline()
                        continue
                    if not line.startswith("\t"):
                        break
                    if line.strip().startswith(device[2:]):
                        return " ".join(line.split()[1:])
                    line = f.readline()
        return ""

if __name__ == "__main__":
    if_names = os.listdir(net_class_dir)
    if "lo" in if_names:
        if_names.remove("lo")

    for ifname in if_names:
        iface = NetIf(ifname)
        if iface.carrier_on():
            print('AddToMenu %s %%status/16/gnome-netstatus-idle.png%%"%s" Nop' % (sys.argv[1], iface.get_desc()))
        else:
            print('AddToMenu %s %%status/16/gnome-netstatus-disconn.png%%"%s" Nop' % (sys.argv[1], iface.get_desc()))
