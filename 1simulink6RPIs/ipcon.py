# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:14:40 2019

@author: kst
"""

class ipconfigs:
    port = 62
    
    party_addr =  [['192.168.100.2',  62], #P0
                  ['192.168.100.3',  62], #P1
                  ['192.168.100.7', 62], #P2
                  ['192.168.100.8', 62], #P3
                  ['192.168.100.10', 62], #Pump1
                  ['192.168.100.11', 62]  #Pump2
                  ]
    
    ccu_adr = '192.168.100.246'
    
    server_addr = [[ccu_adr, 4002], #P0
                   [ccu_adr, 4003], #P1
                   [ccu_adr, 4007], #P2
                   [ccu_adr, 4008], #P3
                   [ccu_adr, 4010], #Reciever 4
                   [ccu_adr, 4011]  #Reciever 5
                  ]