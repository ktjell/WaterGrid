# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 10:59:17 2020

@author: kst
"""

import tkinter as tk
from tkinter import ttk
import queue as que
import time


        
def ShowChoice():
        if not q2.full():
            q2.put(v.get())

def putinque(val):
    if not q.full():
        q.put(val)

def gui(root):
    
    root.geometry("80x420")
#        self.root.protocol("WM_DELETE_WINDOW", self.callback)
    
    
    w = tk.Scale(root, from_=2, to=0, command = putinque)
    w.set(3)
    w.grid(row = 0, column = 2)

    label = tk.Label(root, text="Cons-", wraplength = 1,font=('Helvetica', 12, 'bold'))
    label.grid(row = 0, column = 0)
    labelt = tk.Label(root, text="umtion", wraplength = 1,font=('Helvetica', 12, 'bold'))
    labelt.grid(row = 0, column = 1)
#        
    choices = [
        "Off",
        "On",
        "Const."
    ]
    
    label1 = tk.Label(root, 
             text="Pump-",wraplength=1,font=('Helvetica', 12, 'bold'), 
             justify = tk.LEFT,
             pady = 20)
    label1.grid(row = 1, column = 0, rowspan = 3)
    labels = tk.Label(root, 
             text="setting",wraplength=1, font=('Helvetica',12, 'bold'),
             justify = tk.LEFT,
             pady = 20)
    labels.grid(row = 1, column = 1, rowspan = 3)
    
#    chk = ttk.Checkbutton(root, text="Off", val = 1, command = ShowChoice)
#    chk.grid(column=2, row=3)
    for c, val in enumerate(choices):
        b = tk.Radiobutton(root, 
                      text=val,
                      padx = 20,
                      justify = tk.LEFT,
                      variable = v,
                      command=ShowChoice,
                      value=c)

        b.grid(row=c+1, column = 2,sticky = tk.W)
#        
    
#    


if __name__ == '__main__':
    
    root = tk.Tk()
    v = tk.IntVar()
    v.set(1)  # initializ
    q = que.LifoQueue()
    q2 = que.LifoQueue()
    
    app = gui(root)
    root.mainloop()

    while not q.empty():
        print('Consumption is: ', q.get())
#        while not q.empty():
#            q.get()
    while not q2.empty():
        print('Pump setting is: ', q2.get())
#        while not q2.empty():
#            q2.get()
            
            
    time.sleep(1)

    