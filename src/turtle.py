#!/usr/bin/env python

import rospy
import numpy as np
import std_msgs
from math import *
from geometry_msgs.msg import Twist, Vector3
from turtlesim.srv import TeleportAbsolute

def turtlerun():
    #T = input('PLease enter the number of T:')
    pub = rospy.Publisher('/turtlesim1/turtle1/cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(50) 
    
    rospy.wait_for_service('/turtlesim1/turtle1/teleport_absolute')
    start = rospy.ServiceProxy('/turtlesim1/turtle1/teleport_absolute',TeleportAbsolute)
    start(5.5,5.5,0.5)	

    T = rospy.get_param("turtlesim1/T")

    t0 = rospy.get_time()

    while not rospy.is_shutdown():
        now_time = rospy.get_time()
        t = now_time-t0
        x = 3*sin((4*pi*t)/T)
        y = 3*sin((2*pi*t)/T)
        dx = 12*pi*cos((4.0*pi*t)/T)/T
        dy = 6*pi*cos((2.0*pi*t)/T)/T
        v = sqrt(dx*dx+dy*dy)
        dx2 = -48*pi*pi*sin((4*pi*t)/T)/(T*T)
        dy2 = -12*pi*pi*sin((2*pi*t)/T)/(T*T)
        w = ((dx*dy2)-(dy*dx2)) /((dx*dx) + (dy*dy))
        
        turtlemove = Twist(Vector3(v,0,0),Vector3(0,0,w))
        rospy.loginfo(turtlemove)
        pub.publish(turtlemove)

        rate.sleep() 

if __name__ == '__main__':
    try:
        rospy.init_node('turtlerun', anonymous=True)
        turtlerun()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
