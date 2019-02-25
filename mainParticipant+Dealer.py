# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:59:42 2018

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

party_addr = [['192.168.100.31', 62], #P0
              ['192.168.100.40', 62], #P1
              ['192.168.100.41', 62], #P2
              ['192.168.100.50', 62] #P3
              ]

ccu_adr = '192.168.100.245'

server_addr = [[ccu_adr, 4010], #P0
               [ccu_adr, 4011], #P1
               [ccu_adr, 4030], #P2
               [ccu_adr, 4031],               #P3
               [ccu_adr, 4040],               #Reciever 4
               [ccu_adr, 4041]                #Reciever 5
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
         if not q.full():
            q2.put(Rx_data)

      udpsock.close()
      print("Exiting " + self.name)

class dealer():
    def __init__(self,F, n, t, numTrip):
        self.n = n
        b = ss.share(F,np.random.choice([-1,1]), t, n)
        self.distribute_shares('b', b)
        triplets = [proc.triplet(F,n,t) for i in range(numTrip)]
        for i in range(n):
            l = []
            for j in range(numTrip):
                l.append(triplets[j][i])
            sock.TCPclient(party_addr[i][0], party_addr[i][1], ['triplets' , l])
        
    def distribute_shares(self, name, s):
        for i in range(self.n):
            sock.TCPclient(party_addr[i][0], party_addr[i][1], [name , int(str(s[i]))])


m = 7979490791
mm = 97
F = field.GF(m)            
n = 4
t = 1
x = 5 #np.random.randint(0,50,40)

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = party_addr.index([ipv4, port])
q = que.Queue()
q2 = que.Queue()
q3 = que.Queue()

#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
UDP_PORT2 = 3000
server_info = party_addr[pnr] #(TCP_IP, TCP_PORT)
server2_info = (server_info[0], UDP_PORT2)

# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
#t2_commsSimulink = UDPcommsThread(2, "t2_commsSimulink", server2_info)
p = party(F,int(x),n,t, pnr, q, q2, party_addr, server_addr)

# Start new Threads
#t2_commsSimulink.start()
t1_comms.start()

for i in party_addr:
    while True:
        try:
            sock.TCPclient(i[0], i[1], ['flag', 1])
            break
        except:
            continue

deal = dealer(F,n,t,50)
p.start()







