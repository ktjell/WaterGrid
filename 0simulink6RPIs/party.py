# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:10:12 2018

@author: kst
"""


import numpy as np
from threading import Thread
import shamir_scheme as ss
import proc
import TcpSocket5 as sock
import queue as que
import time
ite = 1800
np.random.seed(2)
#dd = np.random.randint(30, size=ite)

class party(Thread):
    def __init__(self, F, x, n, t, i, q, q2,q3,q4, paddr, saddr):
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
        self.q4 = q4
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
    def get_triplets(self):
        while 'triplets' not in self.recv:
            self.readQueue()
        b = self.recv['triplets']
        res = []
        for i in b:
            res.append([self.F(j) for j in i])
        self.triplets = res
    
    def mult_shares(self, a, b):
        r = self.triplets[self.c]
        self.c += 1
        
        d_local = a - r[0]
        self.broadcast('d' + str(self.comr), d_local)
        d_pub = self.reconstruct_secret('d' + str(self.comr))
        self.comr +=1
        
        e_local = b - r[1]
        self.broadcast('e' + str(self.comr), e_local)
        e_pub = self.reconstruct_secret('e' + str(self.comr))
        self.comr+=1
        
        return d_pub * e_pub + d_pub*r[1] + e_pub*r[0] + r[2]
    
    def legendreComp(self,a,b):
        r = self.triplets[self.c]
        self.c+=1
        t = self.tt
        g = a - b
        k = self.mult_shares(t, self.mult_shares(r[0], r[0]))
        j_loc = self.mult_shares(g, k)
        self.broadcast('j'+ str(self.comr), j_loc)
        j_pub = self.reconstruct_secret('j'+str(self.comr))
        self.comr+=1
        
        ex = (self.F.p-1)/2
        sym = pow(int(str(j_pub)),int(ex), self.F.p)
        f = sym * t
        c = self.mult_shares((f+1), self.F(2).inverse())
        return c
    
    def run(self):
        print('Consumer ', self.i+1, ' online')
        self.get_triplets()
        self.tt = self.get_share('b')
        
## DISTRIBUTE INPUT
        for j in range(ite):
#            data = dd[j]
#            print('Data: ', data)
            while True:
                if not self.q2.empty():
                    dat = self.q2.get()
                    break
            try:
#                CtrPres
                data = int(dat[0]*100)
                if j >0:
                    self.q4.put([1,dat[1]])
            except:
                print(j)
                data = int(dat*100)
                
            print('measured pressure:', data/100)
            
#            data = data
            self.distribute_shares(data)

    ## GET INPUT_SHARES  
            input_shares = self.get_shares('input')
            
    # Find minimum using Legendre Comparison:
            c = self.legendreComp(input_shares[0], input_shares[1])             
            a = self.mult_shares(1-c,input_shares[0]) + self.mult_shares(c,input_shares[1])            
            temp = a
            for i in range(2,4):
                    c = self.legendreComp(a, input_shares[i])
                    a = self.mult_shares(1-c,a)+self.mult_shares(c,input_shares[i])
            
            output4 = temp - a # booster 1 4
            
            output1 = a # Booster 2  # 1
            output2 = input_shares[0] - output1   # cons 3 2
            output3 = input_shares[1] - output1  # cons 4 3
                        
            output5 = input_shares[2] - output1 - output4 # cons 1 5
            output6 = input_shares[3] - output1 - output4 # cons 2 6 
            
            outputMATLAB = [output1, output2, output3, output4, output5, output6]
            outputLOCAL = [output6, output5, output3, output2, output4, output1]
            
            for i in range(len(outputMATLAB)):
                sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], ['outputMAT' + str(self.i) , int(str(outputMATLAB[i])) ])
                sock.TCPclient(self.party_addr[i][0], self.party_addr[i][1], ['outputLOC' + str(self.i) , int(str(outputLOCAL[i]))  ])            
            outMAT = int(str(self.reconstruct_secret('outputMAT'))) / 100.
            outLOC = int(str(self.reconstruct_secret('outputLOC'))) / 100.
            sock.UDPclient(self.server_addr[self.i][0], self.server_addr[self.i][1], outMAT)
            print('Control output party {}, round {}: {}'.format(self.i,j, outLOC))
            self.q4.put([2,outLOC])
#            time.sleep(1)
            #self.recv = {}
            self.c = 0
            self.comr = 0
        