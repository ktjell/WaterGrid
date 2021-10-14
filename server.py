# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 12:52:35 2020

@author: kst
"""

import socket
from ipcon import ipconfigs as ips

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))


while True:
    full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")

    if len(full_msg) > 0:
        print(full_msg)