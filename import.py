# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 08:05:27 2017

@author: jeffr
"""

import xlrd
import pydot

book = xlrd.open_workbook("UC San Diego.xlsx")
sh = book.sheet_by_index(0)

courseList = []

for rx in range(sh.nrows):
    if rx != 1:
        aCourse = Course(sh.cell(rx,1), sh.cell(rx,2), sh.cell(rx,3), sh.cell(rx,4), sh.cell(rx,5))
        courseList.append(aCourse)
        
