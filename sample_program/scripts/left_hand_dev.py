#!/usr/bin/env python                                                           
import rospy
from geometry_msgs.msg import Twist
from raspimouse_ros_2.msg import *

class left_hand():
 def __init__(self):
  self.sub = rospy.Subscriber('/lightsensors', LightSensorValues, self.callback_ls)

  self.l = [0,0,0,0]
  self.vel = Twist()
  self.trigger = False

 def callback_ls(self, msg):
  self.l[0]=msg.right_forward
  self.l[1]=msg.right_side
  self.l[2]=msg.left_side
  self.l[3]=msg.left_forward
  print (self.l)

 def my_callback(self,event):
#  print 'Timer called at ' + str(event.last_duration)
  print (self.l)

 def lsv_step(self,val):
  rospy.Timer(rospy.Duration(0.7), self.ls_pub, oneshot=True)
  rospy.Timer(rospy.Duration(0.3), self.ls_pub2, oneshot=True)

 def ls_pub(self, val):
  self.vel.linear.x = 0.35
  pub.publish(self.vel)
  

 def ls_pub2(self, val):
  if self.trigger == False:
   self.trigger = True
  elif self.trigger == True:
   self.vel.linear.x = 0.0
   pub.publish(self.vel)

if __name__ == "__main__":
 rospy.init_node('sample')
 pub = rospy.Publisher('/cmd_vel',Twist,queue_size = 10)
 l = left_hand()
 rospy.Timer(rospy.Duration(1), l.lsv_step, oneshot=False)
 rospy.spin()
