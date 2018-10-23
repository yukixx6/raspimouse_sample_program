#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, rospy, time
from raspimouse_ros_2.msg import *

class Left_hand():
 def __init__(self):
  self.sub = rospy.Subscriber('/lightsensors', LightSensorValues, self.callback_ls)
  self.time = 0.0
  self.ls_time = 0.0
  self.write_time = 0.0
  self.status = 0
  self.ls_val = [0, 0, 0, 0, 0, 0]

 def time_set(self):
  self.time = rospy.get_time()

 def callback_ls(self, value):
  if self.ls_time + 0.8 <= self.time:
   self.ls_val = value
   self.now = self.time
  self.time_set()
  self.motor_status(self.ls_val)
  #print(self.ls_val)

 def motor_status(self, data):
  try:
   if data.left_side<data.right_forward and data.left_side<data.right_side:
    self.status = 1 
   elif data.sum_forward<data.right_side+data.left_side and data.sum_all<4000:
    self.status = 2
   elif data.right_side<data.right_forward and data.right_side<data.left_side and data.right_side<left_forward:
    self.status = 3
   else:
    self.status = 4
   self.write_to_file(self.status)
  except:
   rospy.logerr("cannot status")
  #print(self.status)

 def write_to_file(self, data):
  try:
   self.time_set()
   self.ls_time = self.time
   self.write_time = self.time
   while self.write_time+1.0 >= self.time:
    with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
     if data == 1:
      lf.write(str(int(round(-204)))+"\n"), rf.write(str(int(round(204)))+"\n")
      #print("right")
     elif data == 2:
      lf.write(str(int(round(495)))+"\n"), rf.write(str(int(round(495)))+"\n")
      print("go")
     elif data == 3:
      lf.write(str(int(round(204)))+"\n"), rf.write(str(int(round(-204)))+"\n")
      #print("left")
     elif data == 4:
      lf.write(str(int(round(409)))+"\n"), rf.write(str(int(round(-409)))+"\n")
      #print("U turn")
    self.time_set()
    #print(self.write_time+1.0-self.time)
   self.write_time = self.time
   while self.write_time+0.5>=self.time:
    self.reset()
    self.time_set()
   self.write_time = self.time
  except:
   rospy.logerr("cannot write to rtmotor_raw_*")

 def reset(self):
  try:
   with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
    lf.write(str(int(round(0)))+"\n"), rf.write(str(int(round(0)))+"\n")
    #print("reset")
  except:
   pass

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 l = Left_hand()
 l.time_set()
 l.ls_time = l.time
 l.write_time = l.time
  #l.reset()
  #rospy.spin()
 rospy.spin()
