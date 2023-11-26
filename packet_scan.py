from scapy.all import sniff, ICMP, IP
import tkinter
from tkinter import messagebox

icmp_dict = {}

root = tkinter.Tk()
root.withdraw()

'''
arp_callback() determines if the packet that has been received is an ARP packet.

params:
packet - a packet that has been received by a host
'''
def arp_callback(packet):
    if packet.haslayer(ICMP):
        print(packet.summary())
    if packet.haslayer(ICMP) and packet.haslayer(IP):
        source_ip = packet[IP].src
        print(f"Source IP: {source_ip}")
        if source_ip in icmp_dict:
            icmp_dict[source_ip] = icmp_dict[source_ip] + 1
        else:
            icmp_dict[source_ip] = 1

# sniffing the packets that are being received for 60 seconds
sniff(prn=arp_callback, store=False, filter="icmp", timeout=60)
print("out")
print(icmp_dict)

for count in icmp_dict.values():
    if count > 5:
        messagebox.showwarning("potential arp poisoning", "POTENTIAL ARP POISONING ATTACK OCCURING. REQUIRES FURTHER INVESTIGATION")
