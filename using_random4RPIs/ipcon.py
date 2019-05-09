# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:14:40 2019

@author: kst
"""

class ipconfigs:
    port = 62
    
    part_addr =  [['192.168.100.7',  62], #P0
                  ['192.168.100.8',  62], #P1
                  ['192.168.100.10', 62], #P2
                  ['192.168.100.11', 62]  #P3
                  ]
    
    ccu_adr = '192.168.100.246'
    
    server_addr = [[ccu_adr, 4031], #P0
                   [ccu_adr, 4040], #P1
                   [ccu_adr, 4041], #P2
                   [ccu_adr, 4050], #P3
                   [ccu_adr, 4060], #Reciever 4
                   [ccu_adr, 4061]  #Reciever 5
                  ]