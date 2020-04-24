# !/usr/bin/env python

import subprocess
import optparse
import re


def mac_changer(interface, new_mac):
    # print("[+] Changing MAC Address of Interface " + interface)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its Mac Address")
    parser.add_option("-m", "--mac-address", dest="new_mac", help="New Mac Address xx:xx:xx:xx:xx:xx")
    (values, options) = parser.parse_args()
    if not values.interface:
        parser.error("[-] Please Specify an Interface, Use --help for more info")
    elif not values.new_mac:
        parser.error("[-] Please Specify a new MAC Address, Use --help for more info")
    return values


def get_current_mac(interface_input):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
    if mac_search:
        return mac_search.group(0)
    else:
        print("[-] Could not able to read the MAC Address")
        exit()


values = get_arguments()

interface = values.interface
new_mac = values.new_mac

current_mac = get_current_mac(interface)
print("[+] Current MAC of " + interface + " is " + str(current_mac))

mac_changer(interface, new_mac)

current_mac = get_current_mac(interface)

if current_mac == new_mac:
    print("[+] Mac Address of " + interface + " is Successfully Changed to " + new_mac)
else:
    print("[-] Could not able to change the MAC Address")
