# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:31:50 2018

@author: kst
"""

import socket
import numpy as np
from threading import Thread
import FFArithmetic as field
import shamir_scheme as ss
import proc
import TcpSocket5 as sock
import time
import queue as que
from participantCode import party
import os

port = 62
party_addr = [['192.168.100.1', 62], #P0 -- NO PLOT
              ['192.168.100.2', 62], #P1
              ['192.168.100.3', 62], #P2
              ['192.168.100.4', 62], #P3 -- NOT PLOT
              ['192.168.100.5', 62], #Receiver 4
              ['192.168.100.6', 62], #Reciever 5
              ]

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
mm = 97
F = field.GF(m)            
n = 4
t = 1
x = 5 #np.random.randint(0,50,40)

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = party_addr.index([ipv4, port])

q = que.Queue()
q2 = que.LifoQueue()


#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
UDP_PORT2 = 3000
server_info = party_addr[pnr ]#(TCP_IP, TCP_PORT)
server2_info = (server_info[0], UDP_PORT2)

# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
t2_commsSimulink = UDPcommsThread(2, "t2_commsSimulink", server2_info)
p = party(F,int(x),n,t,pnr, q, q2)

# Start new Threads
t2_commsSimulink.start()
t1_comms.start()

for i in party_addr:
    while True:
        try:
            sock.TCPclient(i[0], i[1], ['flag', 1])
            break
        except:
            time.sleep(.1)
            continue

p.start()







