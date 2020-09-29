# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:31:50 2018

@author: kst
"""

import socket
import numpy as np
from threading import Thread
import tkinter as tk
import FFArithmetic as field
import shamir_scheme as ss
import proc
import TcpSocket5 as sock
import time
import queue as que
from party import party
from plotter import plotter
from gui import gui

import os
from ipcon import ipconfigs as ips


class commsThread (Thread):
   stop = False  
   def __init__(self, threadID, name, server_info,q):
      Thread.__init__(self)
      self.q = q
      self.threadID = threadID
      self.name = name
      self.server_info = server_info  # (Tcp_ip, Tcp_port)
      self.Rx_packet = [] # tuple [[client_ip, client_port], [Rx_data[n]]]

   def run(self):
#      print("Starting " + self.name)      
      #Create TCP socket
      tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      tcpsock.bind(tuple(self.server_info))
      #Communication loop - Wait->Receive->Put to queue
      while not self.stop:
         Rx_packet = sock.TCPserver(tcpsock)
#         print("Client info:",Rx_packet[0])
#         print("Data recv:",Rx_packet[1])
         if not self.q.full():
            self.q.put(Rx_packet)
      print("Exiting " + self.name)

class UDPcommsThread(Thread):
   def __init__(self, threadID, name, server_info):
      Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.server_info = server_info  # (Tcp_ip, Tcp_port)
      self.Rx_packet = []  # tuple [[client_ip, client_port], [Rx_data[n]]]

   def run(self):
      print("Starting " + self.name)
      #Create UDP socket
      udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      udpsock.bind((self.server_info[0], self.server_info[1]))
      print('UDP Server Started:', self.server_info[0], self.server_info[1])

      #Communication loop - Wait->Receive->Put to queue
      while True:
         Rx_data = sock.UDPserver(udpsock)
         if not q2.full():
             q2.put(int(Rx_data*100))

      udpsock.close()
      print("Exiting " + self.name)

        
m = 7979490791
F = field.GF(m)            
n = 4
t = 1
x = 5

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = ips.party_addr.index([ipv4, ips.port])
q = que.Queue()
q2 = que.Queue()
q3 = que.Queue()
q4 = que.Queue()
qin1 = que.LifoQueue()
qin2 = que.LifoQueue()

#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
UDP_PORT2 = 3000
server_info = ips.party_addr[pnr]#(TCP_IP, TCP_PORT)
server2_info = (ipv4, UDP_PORT2)

# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
t2_commsSimulink = UDPcommsThread(2, "t2_commsSimulink", server2_info)
ploting = plotter(q3,q4,m)
ploting.start()

#ploting2 = plotter2(q4)
#ploting2.start()

p = party(F,int(x),n,t,pnr, q, q2, q3, q4,qin1,qin2, ips.party_addr, ips.server_addr)

# Start new Threads
t2_commsSimulink.start()
t1_comms.start()

for i in ips.party_addr:
    while True:
        try:
            sock.TCPclient(i[0], i[1], ['flag', 1])
            break
        except:
            time.sleep(1)
            continue

p.start()

app = gui(qin1, qin2)
