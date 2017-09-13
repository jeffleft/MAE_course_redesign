# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 08:05:27 2017

@author: jeffrey
"""

import xlrd
import pydot

class Course:

    cList = []

    def __init__(self, name, title, units, category, prereq, coreq):
        self.name = name
        self.title = title
        self.units = units
        self.prereq = prereq
        self.coreq = coreq
        self.category = category

        self.cList.append(self)

    def findDependencies(self):

        self.dList = []
        
        for aCourse in self.cList:
            if self.name in aCourse.prereq:
                self.dList.append(aCourse.name)
                aCourse.print()
        
        self.dnum = len(self.dList)

    def findCourse(self, name):
        for aCourse in self.cList:
            if name == aCourse.name:
                return(aCourse)
        
    def clearList(self):
        self.cList = []
        
    def print(self):
        print(self.name, ". ", self.title, " (", self.units, ")", sep="")
        print("Prerequisites:", self.prereq)
        
def scomp(str1, str2):
    total = max(len(str1),len(str2))
    matched = 0
    
    for i in range(0,min(len(str1),len(str2))):
        if str1[i] == str2[i]:
            matched = matched + 1
            
    return matched/total
        
# Open workbook
book = xlrd.open_workbook("./Curriculum2/Brown University/Brown University.xlsx")
sh = book.sheet_by_index(0)

courseList = []

# import courses
for rx in range(sh.nrows):
    if rx != 0:
        #               Name            Title           Units       FE Category     Prereq      Coreq
        aCourse = Course(sh.cell(rx,0).value, sh.cell(rx,1).value, sh.cell(rx,2).value,
                         sh.cell(rx,3).value.split(",") if isinstance(sh.cell(rx,3).value,str) else sh.cell(rx,3).value, 
                         sh.cell(rx,4).value.split(",") if isinstance(sh.cell(rx,4).value,str) else sh.cell(rx,4).value,
                         sh.cell(rx,5).value.split(",") if isinstance(sh.cell(rx,5).value,str) else sh.cell(rx,5).value)
        courseList.append(aCourse)
        
# create dot graph
graph = pydot.Dot(graph_type='digraph', rank_dir = 'LR')
nodeList = []

# create nodes (classes)
for pCourse in courseList:

    # assign color based on FE category (1-15)
    colors = ['#99FFCC', '#CCCC99', '#CCCCCC', '#CCCCFF', '#CCFF99', '#CCFFCC', '#CCFFFF', '#FFCC99', '#FFCCCC', '#FFCCFF', '#FFFF99', '#FFFFCC', '#70a6ff', '#ffcc70', '#f3baff']
    color = 'gray' 
    if isinstance(pCourse.category, float):
        color = colors[int(pCourse.category)-1]
    else:
        if not pCourse.category[0] == '':
            color = colors[int(pCourse.category[0])-1]
            
    
    # ranks nodes by number of dependencies (idk if worth)
    pCourse.findDependencies()
    #nodex = pydot.Node(pCourse.name, style = 'filled', shape = 'box', rank = pCourse.dnum, fillcolor = color)
    nodex = pydot.Node(pCourse.name, style = 'filled', shape = 'box', fillcolor = color)
    nodeList.append(nodex)
    
# create subgraphs
lower_div = pydot.Cluster('LD', label = 'Lower Division', rank = 'min')
upper_div = pydot.Cluster('UD', label = 'Upper Division', rank = 'max')
    
# draw arrow from prereq to course    
for nodex in nodeList:
    # add node to cluster
    if int(''.join(filter(str.isdigit, nodex.get_name()))) < 100:
        lower_div.add_node(nodex)
    else:
        upper_div.add_node(nodex)
    
    # find corr. course
    b = pCourse.findCourse(nodex.get_name()[1:-1])
#    b.print()
    
    for preq in b.prereq:
            # find courses that match prereq name
        for nodey in nodeList:
            if nodey.get_name()[1:-1] == preq:
                # weight edge by similarity of name
                graph.add_edge(pydot.Edge(nodey, nodex, weight = scomp(nodey.get_name()[1:-1],preq)*1000))
#                print("edge added")
#    graph.add_node(nodex)

graph.add_subgraph(lower_div)
graph.add_subgraph(upper_div)
    
graph.write_png('Brown University.png')