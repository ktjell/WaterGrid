# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:13:01 2019

@author: kst
"""

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
from participantCodePLOT4SIMU import party
import matplotlib.pyplot as plt
import os
import ipcon.ip_configs as ips



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
        else:
           return ydata

        # after the figure, axis, and line are created, we only need to update the y-data
        line.set_ydata(ydata)
        self.fig.canvas.draw()
        return ydata
        
m = 7979490791
F = field.GF(m)            
n = 4
t = 1
x = 5
port = ips.port
ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
pnr = ips.part_addr.index([ipv4, port])
q = que.Queue()
q2 = que.Queue()
q3 = que.Queue()

#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
server_info = ips.part_addr[pnr]#(TCP_IP, TCP_PORT)


# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
ploting = plotter(q3)
ploting.start()
p = party(F,int(x),n,t,pnr, q, q2, q3, ips.part_addr)

# Start new Threads
t1_comms.start()

for i in ips.part_addr:
    while True:
        try:
            sock.TCPclient(i[0], i[1], ['flag', 1])
            break
        except:
            time.sleep(1)
            continue

p.start()







