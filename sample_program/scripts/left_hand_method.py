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
 #print(data)
 try:
  with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
   if data[2] >= 500 and data[0]+data[3] > 2000 and data[1] > 500:
    lf.write(str(int(round(180)))+"\n"), rf.write(str(int(round(-180)))+"\n")
    print("↓")
    print(data)
   elif data[2] >= 500 and data[0]+data[3] > 2000 and data[0]+data[1] <= 2000 and data[2]+data[3] > 2000:
    lf.write(str(int(round(90)))+"\n"), rf.write(str(int(round(45)))+"\n")
    print("→")
    print(data)
   elif 1500 >= data[2] >= 500 and data[0]+data[3] <= 2000 :
    lf.write(str(int(round(100)))+"\n"), rf.write(str(int(round(100)))+"\n")
    print("↑")
    print(data)
   elif data[2] < 500 and sum(data) > 400:
    lf.write(str(int(round(45)))+"\n"), rf.write(str(int(round(90)))+"\n")
    print("←")
    print(data)
   else:
    lf.write(str(int(round(100)))+"\n"), rf.write(str(int(round(100)))+"\n")
   print(data)
 except:
  rospy.logerr("cannot write to raw_file")

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 rate = rospy.Rate(1)
 while not rospy.is_shutdown():
  lsf_listener()
  #motor_vel()
  rate.sleep()
