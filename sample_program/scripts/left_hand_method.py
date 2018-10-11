#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,math
import rospy

from geometry_msgs.msg import Twist
from raspimouse_ros_2.msg import LightSensorValues
from raspimouse_ros_2.msg import MotorFreqs

class Motor:
 def __init__(self):
  self.motor_sw = 0
  sub = rospy.Subscriber('lightsensor_values', LightSensorValues, self.callback_ls_val)
  pub = rospy.Publisher('/raspimouse_on_gazebo/diff_drive_controller/cmd_vel', Twist, queue_size=10)

 def callback_ls_val(self, message):
  ls_val = message()
  try:
   if ls_val.left_side < 1200:
    self.motor_sw = 1
   elif ls_val.left_side >= 1200 and ls_val.sum_forward <= 2000:
    self.motor_sw = 2
   elif ls_val.ls_val.left_side >= 1200 and ls_val.sum_forward > 2000 and ls_val.right_side <= 1200:
    self.motor_sw = 3
   elif ls_val.ls_val.left_side >= 1200 and ls_val.sum_forward > 2000 and ls_val.right_side > 1200:
    self.motor_sw = 4
   else:
    self.motor_sw = 0
  except: 
   rospy.logerr("cannot subscrib")

 def motor_vel(self):
  vel = Twist()
  if self.motor_sw == 0:
   vel.linear.x = 0.35
  elif self.motor_sw == 1:
   vel.angular.z = 3.21
  elif self.motor_sw == 2:
   vel.linear.x = 0.35
  elif self.motor_sw == 3:
   vel.angular.z = -3.21
  elif self.motor_sw == 4:
   vel.angular.z = -6.42
  pub.publish(vel)

if __name__ == "__main__":
 rospy.init_node("aaa")
 motor = Motor()
 swfile ="/dev/rtmotoren0"
 motor
 rospy.spin()
