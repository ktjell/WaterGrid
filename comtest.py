# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:28:45 2020

@author: kst
"""

import socket
from ipcon import ipconfigs as ips

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = ips.party_addr.index([ipv4, ips.port])

HOST = ips.party_addr[pnr] # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST))

#Lets loop awaiting for your input
while True:
	command = raw_input('Enter your command: ')
	s.send(command)
    reply = s.recv(1024)
    if reply == 'Terminate':
        break
	print(reply)