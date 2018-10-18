#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, rospy

def lsf_listener():
 try:
  with open("/dev/rtlightsensor0", 'r') as f:
   data = f.readline().split()
   data = [int(e) for e in data]
   print(data)
   motor_vel(data) 
 except:
  rospy.logerr("cannot open rtlightsensor0")

def motor_vel(data):
 try:
  if data[2]<data[0] and data[2]<data[1]:
   status = 1 
  elif data[0]+data[3]<data[1]+data[2] and sum(data)<4000:
   status = 2
  elif data[1]<data[0] and data[1]<data[2] and data[1]<data[3]:
   status = 3
  else:
   status = 4
  #rate = rospy.Rate(1)
  #if not rospy.is_shutdown():
  write_to_file(status)
  #print(status)
   #rate.sleep()
 except:
  pass

def write_to_file(data):
 #print(data)
 try:
  with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
   if data == 1:
    lf.write(str(int(round(-204)))+"\n"), rf.write(str(int(round(204)))+"\n")
    print("right")
   elif data == 2:
    lf.write(str(int(round(495)))+"\n"), rf.write(str(int(round(495)))+"\n")
    print("go")
   elif data == 3:
    lf.write(str(int(round(204)))+"\n"), rf.write(str(int(round(-204)))+"\n")
    print("left")
   elif data == 4:
    lf.write(str(int(round(409)))+"\n"), rf.write(str(int(round(-409)))+"\n")
    print("U turn")
 except:
  rospy.logerr("cannot write to rtmotor_raw_*")

def reset():
 try:
  with open("/dev/rtmotor_raw_l0", 'w') as lf, open("/dev/rtmotor_raw_r0", 'w') as rf:
   lf.write(str(int(round(0)))+"\n"), rf.write(str(int(round(0)))+"\n")
   #print("reset")
 except:
  rospy.logerr("cannot reset")

if __name__ == "__main__":
 rospy.init_node("left_hand_method")
 rate = rospy.Rate(1)
 try:
  while not rospy.is_shutdown():
   if not rospy.is_shutdown():
    lsf_listener()
    rate.sleep()
    reset()
    rate.sleep()
 except:
  pass
