# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:31:50 2018

@author: kst
"""

import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
import queue as que
import random
import time


class plotter(Thread):
    def __init__(self,q):
      Thread.__init__(self)
#      self.line1 = []
      self.x1 = np.arange(-49,1)
      self.x2 = np.arange(-49,1)
      self.x3 = np.arange(-49,1)
      self.x4 = np.arange(-49,1)
      self.y0 = np.zeros(50)-1
      self.y1 = np.zeros(50)-1
      self.y2 = np.zeros(50)-1
      self.y3 = np.zeros(50)-1
      self.q = q
      
    def run(self):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        self.fig = plt.figure(figsize=(13,6))
        self.ax = self.fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line0, = self.ax.plot(self.x1, self.y0,'bo',alpha=0.8)   
        line1, = self.ax.plot(self.x2, self.y1,'ro',alpha=0.8) 
        line2, = self.ax.plot(self.x3, self.y2,'go',alpha=0.8) 
        line3, = self.ax.plot(self.x4, self.y3,'yo',alpha=0.8) 
        #update plot label/title
        self.ax.set_ylim(0,1)
        self.ax.set_ylabel('data')
        self.ax.set_xlabel('time')
        self.ax.set_title('Received data')
        plt.show()
        
        while True:
            if not self.q.empty():
                b = self.q.get()
                print(b)
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
            ydata = np.append(ydata[1:], y)
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


ite = 10000
n = 4

q = que.Queue()

NUMS = []
for i in range(n):
    NUMS.append(np.random.rand(ite))
    

plott = plotter(q)

plott.start()

for i in range(ite):
    indexes = random.sample(range(n), n)
    for j in range(n):
        q.put([str(indexes[j]), NUMS[j][i]])
        





















