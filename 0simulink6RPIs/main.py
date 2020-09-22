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
from party import party
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
         Rx_data = sock.UDPserver(udpsock)[0]
         if not q2.full():
             q2.put(int(Rx_data*100))

      udpsock.close()
      print("Exiting " + self.name)

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

#plot the received values
class plotter(Thread):
    def __init__(self,q1,q2):
      Thread.__init__(self)
#      self.line1 = []
      self.x1 = np.arange(-99,1)
      self.x2 = np.arange(-99,1)
      self.x3 = np.arange(-99,1)
      self.x4 = np.arange(-99,1)
      self.y0 = np.zeros(100)-1
      self.y1 = np.zeros(100)-1
      self.y2 = np.zeros(100)-1
      self.y3 = np.zeros(100)-1
      self.q1 = q1
      self.q2 = q2
      
      self.xdata1 = np.arange(-99,1)
      self.yB = np.zeros(100)
      
      self.xdata2 = np.arange(-99,1)
      self.yA = np.zeros(100)
      
    def run(self):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        self.fig1 = plt.figure(figsize=(13,6))
        self.ax = self.fig1.add_subplot(111)
        
        # create a variable for the line so we can later update it
        line0, = self.ax.plot(self.x1, self.y0,'bo',alpha=0.8)   
        line1, = self.ax.plot(self.x2, self.y1,'ro',alpha=0.8) 
        line2, = self.ax.plot(self.x3, self.y2,'go',alpha=0.8) 
        line3, = self.ax.plot(self.x4, self.y3,'yo',alpha=0.8) 
        self.ax.set_ylim(0,1)
        self.ax.set_ylabel('data')
        self.ax.set_xlabel('time')
        self.ax.set_title('Received data')
        
        
        self.fig2 = plt.figure(figsize=(13,6))
        ax1 = self.fig2.add_subplot(211)
        
        lineA, = ax1.plot(self.xdata1, self.yB,'bo',alpha=0.8)   
        
        #update plot label/title
        ax1.set_ylim(0,1)
        ax1.set_ylabel('data')
        ax1.set_xlabel('time')
        ax1.set_title('Received data')
        
        
        ax2 = self.fig2.add_subplot(212)
        lineB, = ax2.plot(self.xdata2, self.yA,'bo',alpha=0.8)   
        #update plot label/title
        ax2.set_ylim(0,1)
        ax2.set_xlim(left = 0)
        ax2.set_ylabel('data')
#        ax2.set_xlabel('time')
        ax2.set_title('Control input')
        plt.show()
        
        
        while True:
            if not self.q2.empty():
                b2 = self.q2.get()
                if b2[0] ==1:
                    self.xdata1, self.yA = self.ploting2(ax1,lineA, self.xdata1, self.yA, b2[1])
                if b2[0] == 2:
                    self.xdata2, self.yB = self.ploting2(ax2,lineB, self.xdata2, self.yB, b2[1])
                
            if not self.q1.empty():
                b = self.q1.get()
                if b[0] == '0':
                     self.x1, self.y0 = self.ploting(line0, self.x1, self.y0, b[1])
                if b[0] == '1':
                     self.x2, self.y1 = self.ploting(line1, self.x2, self.y1, b[1])                                                                                                                                                                                              
                if b[0] == '2':
                     self.x3, self.y2 = self.ploting(line2, self.x3, self.y2, b[1])
                if b[0] == '3':
                    self.x4, self.y3 = self.ploting(line3, self.x4, self.y3, b[1])
                
            
    def ploting(self, line, xdata, ydata, y):
        if not isinstance(y, list):   #Hvis y IKKE er en list gør:
            ydata = np.append(ydata[1:], y/float(m))
            xdata = xdata + 1

#            if isinstance(y[0], list):
#                return
#            else:
#                yl = self.ydata[len(y):]
#                self.ydata = np.concatenate((yl, np.array(y)/float(m)))
        else:
           return xdata, ydata
            
           
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        self.ax.set_xlim(max(0, min( min(self.x1), min(self.x2),min(self.x3), min(self.x4) )), max( max(self.x1), max(self.x2), max(self.x3), max(self.x4)) +1)
        # adjust limits if new data goes beyond bounds
#        if np.min(self.ydata)<=self.line1.axes.get_ylim()[0] or np.max(self.ydata)>=self.line1.axes.get_ylim()[1]:
#            plt.ylim([np.min(self.ydata)-np.std(self.ydata),np.max(self.ydata)+np.std(self.ydata)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
#        plt.pause(0.1)
        self.fig1.canvas.draw()
        return xdata, ydata
    
    def ploting2(self, ax, line, x,y, b):

        y = np.append(y[1:], b)
        x = x + 1
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line.set_xdata(x)
        line.set_ydata(y)
        ax.set_xlim(max(0,min(x)), max(x)+1)
        ax.set_ylim(0,max(y)+0.1)
        # adjust limits if new data goes beyond bounds
#        if np.min(self.ydata)<=self.line1.axes.get_ylim()[0] or np.max(self.ydata)>=self.line1.axes.get_ylim()[1]:
#            plt.ylim([np.min(self.ydata)-np.std(self.ydata),np.max(self.ydata)+np.std(self.ydata)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
#        plt.pause(0.1)
        self.fig2.canvas.draw()
        return x,y


#            

        
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

#Initialization..
#TCP_IP = '192.168.100.246'
#TCP_PORT = 62
UDP_PORT2 = 3000
server_info = ips.party_addr[pnr]#(TCP_IP, TCP_PORT)
server2_info = (ipv4, UDP_PORT2)

# Create new threads..
t1_comms = commsThread(1, "Communication Thread", server_info,q)
t2_commsSimulink = UDPcommsThread(2, "t2_commsSimulink", server2_info)
ploting = plotter(q3,q4)
ploting.start()

#ploting2 = plotter2(q4)
#ploting2.start()

p = party(F,int(x),n,t,pnr, q, q2, q3, q4, ips.party_addr, ips.server_addr)

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







