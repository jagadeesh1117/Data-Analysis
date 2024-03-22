#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:46:10 2024

@author: jagadeeshchowdary
"""


import time   
import unittest
import datetime
from lift import Building


class Lift_test:
    def __init__(self,levels):
        self.levels=levels
        self.direction=None
        self.current_level=0
        self.selected_levels=set()
    
    def next_action_test(self):
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

class Building_test:
    def __init__(self,levels,no_elevators):
        self.levels=levels
        self.no_elevators=no_elevators
        self.up_inputs=set()
        self.down_inputs=set()
        self.lifts=[Lift_test(levels) for i in range(no_elevators)]
        self.is_done=False

    def take_input_test(self,floor_no,direction):
        if direction=="UP":
            self.up_inputs.add(floor_no)
        else:
            self.down_inputs.add(floor_no)

    def take_lift_input_test(self, lift_no, floor_no):
        if floor_no>=self.levels:
            return "Invalid"
        lift_obj=self.lifts[lift_no]
        if lift_obj.direction==None:
            if floor_no>lift_obj.current_level:
                lift_obj.direction='UP'
            elif floor_no<lift_obj.current_level:
                lift_obj.direction="DW"
        self.lifts[lift_no].selected_levels.add(floor_no)

    def print_current_state_test(self,timestamp):
        result=[]
        c=0
        for i in range(self.no_elevators):
            self.lifts[i].next_action_test()
            c+=len(self.lifts[i].selected_levels)
            result.append("Lift %d l%d %s"%(i,self.lifts[i].current_level,self.lifts[i].direction))
            time.sleep(1)
        if c>0:
            self.is_done=True
        else:
            self.is_done=False
        return result
        

    def total_process_test(self, total_input):
        # print("Process start time", datetime.datetime.now().strftime("%c"))
        result1 = []
        total_input.sort(key=lambda x: x[1])
        

        
        now = datetime.datetime.now()
        timestamp = int(now.timestamp())
        time = int(timestamp)

        
        ind=0
        while time<=total_input[-1][1] or self.is_done:
            while ind<len(total_input) and total_input[ind][1]==time:
                command, timestamp, x, y = total_input[ind]
                if command=="linp":
                    self.take_lift_input_test(x,y)
                else:
                    self.take_input_test(x,y)
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
                        self.take_lift_input_test(nup_min[1],c_floor)
                    else:
                        self.take_lift_input_test(nnon_min[1],c_floor)
                else:
                    if up_min[0]<=non_min[0]:
                        self.take_lift_input_test(up_min[1],c_floor)
                    else:
                        self.take_lift_input_test(non_min[1],c_floor)
            
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
                        self.take_lift_input_test(ndw_min[1],c_floor)
                    else:
                        self.take_lift_input_test(nnon_min[1],c_floor)
                else:
                    if dw_min[0]<=non_min[0]:
                        self.take_lift_input_test(dw_min[1],c_floor)
                    else:
                        self.take_lift_input_test(non_min[1],c_floor)
            self.down_inputs=set()
            result1.append(self.print_current_state_test(time))
            time+=1
        return result1




operator=Building_test(20,2)

now1 = datetime.datetime.now()
timestamp = int(now1.timestamp())
inputs = [("finp", timestamp, 3, "UP")]
answer = operator.total_process_test(inputs)




now1 = datetime.datetime.now()
timestamp = int(now1.timestamp())

inputs = [("finp", timestamp, 3, "UP")]

class BuildingTests(unittest.TestCase):
    def test_total_process(self):
        operator = Building(20, 2)
        output_value = operator.total_process(inputs)

        self.assertEqual(output_value, answer)

# Create a test suite
test_suite = unittest.TestLoader().loadTestsFromTestCase(BuildingTests)

# Create a test runner and run the test suite
test_runner = unittest.TextTestRunner()
test_runner.run(test_suite)
    
    
    
    #sample=[("linp",timestamp,lift_no,floor_no),("finp",timestamp,floor_no,directions)]
# print(datetime.datetime.now().strftime("%c"))
#operator.total_process([("linp",2,1,6),("finp",1,3,"UP"),("finp",1,1,"DW")])