# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 21:17:28 2017

@author: jeffr
"""

def scomp(str1, str2):
    total = max(len(str1),len(str2))
    matched = 0
    
    for i in range(0,min(len(str1),len(str2))):
        if str1[i] == str2[i]:
            matched = matched + 1
            
    return matched/total

print(scomp("MAE 154", "MAE 155"))