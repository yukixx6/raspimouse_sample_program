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
   date = f.readline().split()
   date = [int(e) for e in date]
   motor_vel(date)
 except:
  rospy.logerr("cannot open lightsensor file")

def motor_vel(date):
 #print(date)
 try:
  with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
   if date[2] >= 450 and date[0]+date[3] > 2000 and date[1] > 1200:
    lf.write(str(int(round(-180)))+"\n"), rf.write(str(int(round(180)))+"\n")
    print("↓")
   elif date[2] >= 450 and date[0]+date[3]  > 2000 and date[1] <= 1200:
    lf.write(str(int(round(90)))+"\n"), rf.write(str(int(round(-90)))+"\n")
    print("→")
   elif date[2] >= 450 and date[0]+date[3] <= 2000:
    lf.write(str(int(round(90)))+"\n"), rf.write(str(int(round(90)))+"\n")
    print("↑")
   elif date[2] >= 100:
    lf.write(str(int(round(-45)))+"\n"), rf.write(str(int(round(45)))+"\n")
    print("←")
 except:
  rospy.logerr("cannot write to raw_file")

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 rate = rospy.Rate(10)
 while not rospy.is_shutdown():
  lsf_listener()
  #motor_vel()
  rate.sleep()
