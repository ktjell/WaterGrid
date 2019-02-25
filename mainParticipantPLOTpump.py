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
from pump import party
import matplotlib.pyplot as plt
import os

port = 62

party_addr = [['192.168.100.31', 62], #P0
              ['192.168.100.40', 62], #P1
              ['192.168.100.41', 62], #P2
              ['192.168.100.50', 62], #P3
              ['192.168.100.60', 62], #P3
              ['192.168.100.61', 62]  #P3
              ]

ccu_adr = '192.168.100.246'

server_addr = [[ccu_adr, 4031], #P0
               [ccu_adr, 4040], #P1
               [ccu_adr, 4041], #P2
               [ccu_adr, 4050], #P3
               [ccu_adr, 4060], #Reciever 4
               [ccu_adr, 4061]  #Reciever 5
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
         Rx_data = sock.UDPserver(udpsock)[0]
         if not q2.full():
             q2.put(int(Rx_data*100))

      udpsock.close()
      print("Exiting " + self.name)

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

class plotter(Thread):
    def __init__(self,q):
      Thread.__init__(self)
#      self.line1 = []
      self.xdata = np.arange(0,100)
      self.y0 = np.zeros(100)-1
      self.y1 = np.zeros(100)-1
      self.y2 = np.zeros(100)-1
      self.y3 = np.zeros(100)-1
      self.q = q
      
    def run(self):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        self.fig = plt.figure(figsize=(13,6))
        ax = self.fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line0, = ax.plot(self.y0,'bo',alpha=0.8)   
        line1, = ax.plot(self.y1,'ro',alpha=0.8) 
        line2, = ax.plot(self.y2,'go',alpha=0.8) 
        line3, = ax.plot(self.y3,'yo',alpha=0.8) 
        #update plot label/title
        plt.ylim(0,1)
        plt.ylabel('data')
        plt.xlabel('time')
        plt.title('Received data')
        plt.show()
        
        
        while True:
            if not self.q.empty():
                b = self.q.get()
                if b[0] == '0':
                    self.y0 = self.ploting(line0, self.y0, b[1])
                if b[0] == '1':
                    self.y1 = self.ploting(line1, self.y1, b[1])                                                                                                                                                                                              
                if b[0] == '2':
                    self.y2 = self.ploting(line2, self.y2, b[1])
                if b[0] == '3':
                    self.y3 = self.ploting(line3, self.y3, b[1])
            
    def ploting(self, line, ydata, y):
        if not isinstance(y, list):
            yl = ydata[:-1]
            ydata = np.insert(yl,0, y/float(m))
#            if isinstance(y[0], list):
#                return
#            else:
#                yl = self.ydata[len(y):]
#                self.ydata = np.concatenate((yl, np.array(y)/float(m)))
        else:
           return ydata
            
           
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line.set_ydata(ydata)
        # adjust limits if new data goes beyond bounds
#        if np.min(self.ydata)<=self.line1.axes.get_ylim()[0] or np.max(self.ydata)>=self.line1.axes.get_ylim()[1]:
#            plt.ylim([np.min(self.ydata)-np.std(self.ydata),np.max(self.ydata)+np.std(self.ydata)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
#        plt.pause(0.1)
        self.fig.canvas.draw()
        return ydata
        
m = 7979490791
F = field.GF(m)            
n = 4
t = 1
x = 5

ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = party_addr.index([ipv4, port])
q = que.Queue()
q2 = que.LifoQueue()
q3 = que.Queue()

#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
UDP_PORT2 = 3000
server_info = party_addr[pnr]#(TCP_IP, TCP_PORT)
server2_info = (ipv4, UDP_PORT2)

# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
t2_commsSimulink = UDPcommsThread(2, "t2_commsSimulink", server2_info)
ploting = plotter(q3)
ploting.start()
p = party(F,int(x),n,t,pnr, q, q2, q3, party_addr, server_addr)

# Start new Threads
t2_commsSimulink.start()
t1_comms.start()

for i in party_addr:
    while True:
        try:
            sock.TCPclient(i[0], i[1], ['flag', 1])
            break
        except:
            time.sleep(1)
            continue

p.start()







