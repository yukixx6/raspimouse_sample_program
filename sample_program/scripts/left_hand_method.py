#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,math
import rospy

from geometry_msgs.msg import Twist
from raspimouse_ros_2.msg import LightSensorValues
from raspimouse_ros_2.msg import MotorFreqs

def lsf_listener():
 try:
  with open("/dev/rtlightsensor0", 'r') as f:
   data = f.readline().split()
   data = [int(e) for e in data]
   motor_vel(data)
 except:
  rospy.logerr("cannot open lightsensor file")

def motor_vel(data):
 try:
  if data[2]<500:
   status = 1
  elif data[2]>=500 and data[0]+data[3]<1000:
   status = 2
  elif data[2]>=500 and data[0]+data[3]>=1000 and data[1]<500:
   status = 3
  elif data[2]>=500 and data[0]+data[3]>=1000 and (data[1]>500 and data[2]>500):
   status = 4
  else:
   status = 2
  write_to_file(status)
  print(status)
 except:
  rospy.logerr("cannot status")

def write_to_file(data):
 #print(data)
 try:
  with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
   if data == 1:
    if status_count >= 3:
     lf.write(str(int(round(-90)))+"\n"), rf.write(str(int(round(90)))+"\n")
     status_count = 0
     print("right")
    else:
     lf.write(str(int(round(50)))+"\n"), rf.write(str(int(round(50)))+"\n")
     status_count += 1
     print("go")
     print(status_count)
   elif data == 2:
    lf.write(str(int(round(100)))+"\n"), rf.write(str(int(round(100)))+"\n")
    print("go")
   elif data == 3:
    lf.write(str(int(round(90)))+"\n"), rf.write(str(int(round(-90)))+"\n")
    print("left")
   elif data == 4:
    lf.write(str(int(round(180)))+"\n"), rf.write(str(int(round(-180)))+"\n")
    print("U turn")
 except:
  rospy.logerr("cannot write to raw_file")

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 status_count = 0
 rate = rospy.Rate(1)
 while not rospy.is_shutdown():
  lsf_listener()
  rate.sleep()
