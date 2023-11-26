import os
import time
import tkinter
from tkinter import messagebox

'''
get_arp_cach() runs the arp -a command on the command line and reads the results.
The command only returns the IP and MAC adddresses of each entry in the arp cache.

returns:
a string representation of the arp cache
'''
def get_arp_cache():
    arp_cache = os.popen("arp -a | awk '{print $2, $4}'").read()
    return arp_cache

# determining the starting ARP cache
previous_arp_cache = get_arp_cache()
previous_arp_cache = previous_arp_cache.split("\n")
previous_arp_dict = {}

for addrs in previous_arp_cache:
    if addrs == "":
        previous_arp_cache.remove("")
    else:
        split = addrs.split(" ")
        ip_addr = split[0]
        mac_addr = split[1]
        previous_arp_dict[ip_addr] = mac_addr
print("previous arp dict:")
print(previous_arp_dict)

'''
Running a constant loop that every minute, gets the current arp cache,
creates a dictionary of IP, MAC address key:value pairs, and compares
them to the beginning arp cache dictionary value. If the dictionaries
are not equal, then a message is displayed indicating there might be an
arp attack occurring
'''
while True:
    current_arp_cache = get_arp_cache()
    current_arp_cache = current_arp_cache.split("\n")
    current_arp_dict = {}

    for addrs in current_arp_cache:
        if addrs == "":
            current_arp_cache.remove("")
        else:
            split = addrs.split(" ")
            ip_addr = split[0]
            mac_addr = split[1]
            current_arp_dict[ip_addr] = mac_addr

    if previous_arp_dict != current_arp_dict:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showwarning("potential arp poisoning", "POTENTIAL ARP POISONING ATTACK OCCURING. REQUIRES FURTHER INVESTIGATION")

    time.sleep(10)  # Check every 60 seconds
