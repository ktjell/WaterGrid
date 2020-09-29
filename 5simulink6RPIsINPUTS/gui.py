# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:10:46 2020

@author: kst
"""

import tkinter as tk
import queue as que
import time

import threading

class gui(threading.Thread):
    def __init__(self,root, q, q2):
        threading.Thread.__init__(self)
        self.root = root
        self.q = q
        self.q2 = q2
#        self.v = v
        self.start()
        
    def ShowChoice(self):
        if not self.q2.full():
            self.q2.put(self.v.get())
    
    def putinque(self,val):
        if not self.q.full():
            self.q.put(val)

    def callback(self):
        self.root.quit()

    def run(self):
#        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry("80x420")
        
        
        w = tk.Scale(self.root, from_=2, to=0, command = self.putinque)
        w.set(3)
        w.grid(row = 0, column = 2)

        label = tk.Label(self.root, text="Cons-", wraplength = 1,font=('Helvetica', 12, 'bold'))
        label.grid(row = 0, column = 0)
        labelt = tk.Label(self.root, text="umtion", wraplength = 1,font=('Helvetica', 12, 'bold'))
        labelt.grid(row = 0, column = 1)
#        
        
#        
        self.v = tk.IntVar()
#        self.v.set(1)  # initializing the choice, i.e. Python
#        
        choices = [
            "Off",
            "On",
            "Const."
        ]
        
        label1 = tk.Label(self.root, 
                 text="Pump-",wraplength=1,font=('Helvetica', 12, 'bold'), 
                 justify = tk.LEFT,
                 pady = 20)
        label1.grid(row = 1, column = 0, rowspan = 3)
        labels = tk.Label(self.root, 
                 text="setting",wraplength=1, font=('Helvetica',12, 'bold'),
                 justify = tk.LEFT,
                 pady = 20)
        labels.grid(row = 1, column = 1, rowspan = 3)
        
        for c, val in enumerate(choices):
            b = tk.Radiobutton(self.root, 
                          text=val,
                          padx = 20,
                          justify = tk.LEFT,
                          variable = self.v,
                          command=self.ShowChoice,
                          value=c)

            b.grid(row=c+1, column = 2,sticky = tk.W)
        

#        #
#        while True:
#            if not q.empty():
#                print('Consumption is: ', q.get())
#                while not q.empty():
#                    q.get()
#            if not q2.empty():
#                print('Pump setting is: ', q2.get())
#                while not q2.empty():
#                    q2.get()
#                    
#                    
#            time.sleep(1)
#    



#
#root = tk.Tk()
#
#q = que.LifoQueue()
#q2 = que.LifoQueue()
#
#app = App(root, q,q2)
#
#
#root.mainloop()