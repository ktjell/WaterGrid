# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:33:11 2020

@author: kst
"""
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

#plot the received values
class plotter(Thread):
    def __init__(self,q1,q2,m, B):
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
      self.q1 = q1
      self.q2 = q2
      self.m = m
      self.B = B
      
      self.xdata1 = np.arange(-499,1)
      self.yB = np.zeros(500)
      
      self.xdata2 = np.arange(-499,1)
      self.yA = np.zeros(500)
      
    def run(self):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
                
        self.fig2 = plt.figure(figsize=(13,6))
        
        if self.B:
            ax1 = self.fig2.add_subplot(211)
 
            lineA, = ax1.plot(self.xdata1, self.yB,alpha=0.8, label = 'diff. pressure')   
            
            xpl = np.arange(0,500)
            ypl = 0.3*np.ones(500)
            ax1.plot(xpl,ypl, color = 'black', linestyle = 'dashed', label = 'required pressure')
            ax1.legend()
            #update plot label/title
            ax1.set_xlim(0,500)
            ax1.set_ylabel('bar')
            ax1.set_xlabel('time')
    #        ax1.set_title('Received data')
            ax1.set_ylim(0,0.45)
            
        
            ax2 = self.fig2.add_subplot(212)
            
        else:
            ax2 = self.fig2.add_subplot(111)
        lineB, = ax2.plot(self.xdata2, self.yA,alpha=0.8, label = 'pump pressure')  
        ax2.legend()
        #update plot label/title
#        ax2.set_ylim(0,1)
        ax2.set_xlim(0,500)
#        ax2.set_ylim(0,0.7)
        ax2.set_ylabel('bar')
#        ax2.set_xlabel('time')
#        ax2.set_title('Control input')
        
        self.fig1 = plt.figure(figsize=(13,6))
#        cfm = plt.get_current_fig_manager()
        
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


        
#        cfm.window.attributes('-topmost', False)



        
        plt.show()

        
        while True:
                        
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
            
            if not self.q2.empty():
                b2 = self.q2.get()
                if b2[0] ==1:
                    self.xdata1, self.yA = self.ploting2(ax1,lineA, self.xdata1, self.yA, b2)
                if b2[0] == 2:
                    self.xdata2, self.yB = self.ploting2(ax2,lineB, self.xdata2, self.yB, b2)
                

                
            
    def ploting(self, line, xdata, ydata, y):
        if not isinstance(y, list):   #Hvis y IKKE er en list gør:
            ydata = np.append(ydata[1:], y/float(self.m))
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

        y = np.append(y[1:], b[1])
        x = x + 1
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line.set_xdata(x)
        line.set_ydata(y)
#        ax.set_xlim(max(0,min(x)), max(x)+1)
        if b[0] == 1:
            ax.set_ylim(0,0.45)
#            ax.set_ylim(0,max(y)+3)
        else:
            ax.set_ylim(0,max(y)+0.1)
        # adjust limits if new data goes beyond bounds
#        if np.min(self.ydata)<=self.line1.axes.get_ylim()[0] or np.max(self.ydata)>=self.line1.axes.get_ylim()[1]:
#            plt.ylim([np.min(self.ydata)-np.std(self.ydata),np.max(self.ydata)+np.std(self.ydata)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
#        plt.pause(0.1)
        self.fig2.canvas.draw()
        return x,y
