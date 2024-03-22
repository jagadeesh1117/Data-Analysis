#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:18:14 2024

@author: jagadeeshchowdary
"""

import multiprocessing

def limit_processors(num_processors):
    try:
        multiprocessing.set_start_method('fork')
    except RuntimeError:
        pass
    multiprocessing.cpu_count = lambda: num_processors

# Set the desired number of processors to limit
num_processors = 2

# Limit the number of processors used
limit_processors(num_processors)

import datetime
import time

class Lift:
    def __init__(self,levels):
        self.levels=levels
        self.direction=None
        self.current_level=0
        self.selected_levels=set()
    
    def next_action(self):
        if self.direction=="UP":
            if self.current_level in self.selected_levels:
                self.selected_levels.discard(self.current_level)
            self.current_level+=1
            self.selected_levels.discard(self.current_level)
            ma=0
            if self.selected_levels:
                ma=max(self.selected_levels)
            if self.current_level==min(self.levels,max(self.current_level,ma)):
                if self.selected_levels:
                    self.direction="DW"
                else:
                    self.direction=None
        elif self.direction=="DW":
            if self.current_level in self.selected_levels:
                self.selected_levels.discard(self.current_level)
            self.current_level-=1
            self.selected_levels.discard(self.current_level)
            ma=self.levels
            if self.selected_levels:
                ma=min(self.selected_levels)
            if self.current_level==max(0,min(self.current_level,ma)):
                if self.selected_levels:
                    self.direction="UP"
                else:
                    self.direction=None

class Building:
    def __init__(self,levels,no_elevators):
        self.levels=levels
        self.no_elevators=no_elevators
        self.up_inputs=set()
        self.down_inputs=set()
        self.lifts=[Lift(levels) for i in range(no_elevators)]
        self.is_done=False

    def take_input(self,floor_no,direction):
        if direction=="UP":
            self.up_inputs.add(floor_no)
        else:
            self.down_inputs.add(floor_no)

    def take_lift_input(self, lift_no, floor_no):
        if floor_no>=self.levels:
            return "Invalid"
        lift_obj=self.lifts[lift_no]
        if lift_obj.direction==None:
            if floor_no>lift_obj.current_level:
                lift_obj.direction='UP'
            elif floor_no<lift_obj.current_level:
                lift_obj.direction="DW"
        self.lifts[lift_no].selected_levels.add(floor_no)

    def print_current_state(self,timestamp):
        result=[]
        c=0
        for i in range(self.no_elevators):
            self.lifts[i].next_action()
            c+=len(self.lifts[i].selected_levels)
            time.sleep(1)
        if c>0:
            self.is_done=True
        else:
            self.is_done=False
        return result

    def total_process(self, total_input):
        result1 = []
        # print("Process start time", datetime.datetime.now().strftime("%c"))
        total_input.sort(key=lambda x: x[1])
        

        
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        time = int(timestamp)

        
        ind=0
        while time<=total_input[-1][1] or self.is_done:
            while ind<len(total_input) and total_input[ind][1]==time:
                command, timestamp, x, y = total_input[ind]
                if command=="linp":
                    self.take_lift_input(x,y)
                else:
                    self.take_input(x,y)
                ind+=1
          
            up_min=[float("inf"),None]
            non_min=[float("inf"),None]
            nnon_min=[float("inf"),None]
            nup_min=[float("inf"),None]
            for c_floor in self.up_inputs:
                for lift in range(self.no_elevators):
                    if self.lifts[lift].current_level<=c_floor:
                        if self.lifts[lift].direction=="UP":
                            if up_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                up_min[1]=lift
                                up_min[0]=abs(c_floor-self.lifts[lift].current_level)
                        elif self.lifts[lift].direction==None:
                            if non_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                non_min[1]=lift
                                non_min[0]=abs(c_floor-self.lifts[lift].current_level)
                    else:
                        if self.lifts[lift].direction==None:
                            if nnon_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                nnon_min[1]=lift
                                nnon_min[0]=abs(c_floor-self.lifts[lift].current_level)
                        else:
                            if nup_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                nup_min[1]=lift
                                nup_min[0]=abs(c_floor-self.lifts[lift].current_level)
                
                if min(up_min[0],non_min[0])==float("inf"):
                    if nnon_min[0]==float("inf"):
                        self.take_lift_input(nup_min[1],c_floor)
                    else:
                        self.take_lift_input(nnon_min[1],c_floor)
                else:
                    if up_min[0]<=non_min[0]:
                        self.take_lift_input(up_min[1],c_floor)
                    else:
                        self.take_lift_input(non_min[1],c_floor)
            
            self.up_inputs=set()

            dw_min=[float("inf"),None]
            non_min=[float("inf"),None]
            nnon_min=[float("inf"),None]
            ndw_min=[float("inf"),None]
            for c_floor in self.down_inputs:
                for lift in range(self.no_elevators):
                    if self.lifts[lift].current_level>=c_floor:
                        if self.lifts[lift].direction=="DW":
                            if dw_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                dw_min[1]=lift
                                dw_min[0]=abs(c_floor-self.lifts[lift].current_level)
                        elif self.lifts[lift].direction==None:
                            if non_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                non_min[1]=lift
                                non_min[0]=abs(c_floor-self.lifts[lift].current_level)
                    else:
                        if self.lifts[lift].direction==None:
                            if nnon_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                nnon_min[1]=lift
                                nnon_min[0]=abs(c_floor-self.lifts[lift].current_level)
                        else:
                            if nup_min[0]>abs(c_floor-self.lifts[lift].current_level):
                                ndw_min[1]=lift
                                ndw_min[0]=abs(c_floor-self.lifts[lift].current_level)
                if min(dw_min[0],non_min[0])==float("inf"):
                    if nnon_min[0]==float("inf"):
                        self.take_lift_input(ndw_min[1],c_floor)
                    else:
                        self.take_lift_input(nnon_min[1],c_floor)
                else:
                    if dw_min[0]<=non_min[0]:
                        self.take_lift_input(dw_min[1],c_floor)
                    else:
                        self.take_lift_input(non_min[1],c_floor)
            self.down_inputs=set()
            
            result1.append(self.print_current_state(time))
            time+=1
        print(result1)
        return result1
            
            

#sample=[("linp",timestamp,lift_no,floor_no),("finp",timestamp,floor_no,directions)]
# print(datetime.datetime.now().strftime("%c"))

operator=Building(20,2)

#operator.total_process([("linp",2,1,6),("finp",1,3,"UP"),("finp",1,1,"DW")])

now1 = datetime.datetime.now()
timestamp = int(now1.timestamp())

        

operator.total_process([("finp",timestamp,3,"UP")])
# print("Process end time",datetime.datetime.now().strftime("%c"))

# print(datetime.datetime.now().strftime("%c"))

# now1 = datetime.datetime.now()
# timestamp = int(now1.timestamp())

# operator.total_process([("linp",timestamp,0,7)])
# print("Process end time",datetime.datetime.now().strftime("%c"))

















# for i in range(2):
#     x = input("Enter the command: ")
#     a = x[0]
#     b = int(x[1])
#     c  =int(x[2])
#     d = 


