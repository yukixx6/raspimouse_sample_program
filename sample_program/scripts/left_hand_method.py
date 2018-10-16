#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,math
import rospy

from geometry_msgs.msg import Twist
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
  #if data[2]>=500 and data[0]+data[3]>=1000 and (data[1]>500 and data[2]>500):
    #status = 4
  #elif data[2]>=500 and data[0]+data[3]>=1000 and data[1]<500:
   #status = 3
  #elif data[2]>=500 and data[0]+data[3]<1000:
   #status = 2
  #elif data[2]<500 and 4000>sum(data)>=400:
   #status = 1
  #else:
   #status = 2
  if data[2] > 3000 or (data[3] > 2500 and data[1] > 2500):
   status = 4 
  elif data[0]>150 and data[1]>400:
   status = 3
  elif data[0]+data[3] < 2000 and data[2] > 500:
   status = 2
  elif data[2] < 500 and data[3] < 2000 and sum(data) < 4000:
   status = 1
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
    lf.write(str(int(round(409)))+"\n"), rf.write(str(int(round(409)))+"\n")
    print("right")
   elif data == 2:
    lf.write(str(int(round(990)))+"\n"), rf.write(str(int(round(990)))+"\n")
    print("go")
   elif data == 3:
    lf.write(str(int(round(409)))+"\n"), rf.write(str(int(round(409)))+"\n")
    print("left")
   elif data == 4:
    lf.write(str(int(round(817)))+"\n"), rf.write(str(int(round(-814)))+"\n")
    print("U turn")
   elif data == 0:
    lf.write(str(int(round(0)))+"\n"), rf.write(str(int(round(0)))+"\n")
 except:
  rospy.logerr("cannot write to raw_file")

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 #rate = rospy.Rate(1)
 while not rospy.is_shutdown():
  lsf_listener()
  #rate.sleep()
 #rospy.spin()
