# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 09:01:04 2018

@author: kst
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:10:12 2018

@author: kst
"""


import numpy as np
from threading import Thread
import shamir_scheme as ss
import TcpSocket5 as sock
import queue as que

ite = 1800

class party(Thread):
    def __init__(self, F, x, n, t, i, q, q2,q3, paddr, saddr):
        Thread.__init__(self)
        self.c = 0
        self.comr = 0
        self.recv = {}
        self.F = F
        self.x = x
        self.n = n
        self.t = t
        self.i = i
        self.q = q
        self.q2 = q2
        self.q3 = q3
        self.party_addr = paddr
        self.server_addr = saddr
        
    def distribute_shares(self, sec):
        shares = ss.share(self.F, sec, self.t, self.n)
        for i in range(self.n):
            sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], ['input' + str(self.i) , int(str(shares[i]))])
        
    def broadcast(self, name, s):
        for i in range(self.n):
            sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], [name + str(self.i) , int(str(s))])
                    
    def readQueue(self):
        while not self.q.empty():
            b = self.q.get()[1]
            self.recv[b[0]] = b[1]
            self.q3.put([b[0][-1], b[1]])
    
    def get_shares(self, name):
        res = []
        for i in range(self.n):
            while name + str(i) not in self.recv:
                self.readQueue()    
            res.append(self.F(self.recv[name+str(i)]))
            del self.recv[name + str(i)]              
        return res
            
    def reconstruct_secret(self, name):
        return ss.rec(self.F, self.get_shares(name))
    
    def get_share(self, name):
        while name not in self.recv:
            self.readQueue()
        a = self.F(self.recv[name])
        del self.recv[name]
        return a
       
    def run(self):
        for j in range(ite):          
            out = int(str(self.reconstruct_secret('output'))) / 100
            sock.UDPclient(self.server_addr[self.i][0], self.server_addr[self.i][1], int(out))
            
            print('Control ouput: ', out)
#            time.sleep(1)
#            self.recv = {}
            self.c = 0
            self.comr = 0
        