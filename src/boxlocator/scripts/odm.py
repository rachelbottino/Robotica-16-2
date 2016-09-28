#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import tf
import math
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry

goal_x = 2
goal_y = 1
x = 0
y = 0
angulo = 0

def odm(dado):
	global x
	global y
	global angulo
	quaternion = (
		dado.pose.pose.orientation.x,
		dado.pose.pose.orientation.y, 
		dado.pose.pose.orientation.z, 
		dado.pose.pose.orientation.w)
	euler = tf.transformations.euler_from_quaternion(quaternion)
	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]
	angulo = yaw
	x = dado.pose.pose.position.x
	y = dado.pose.pose.position.y
	#print(euler)



if __name__=="__main__":

	rospy.init_node("odmetria")

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
	recebe_odom = rospy.Subscriber("/odom", Odometry, odm)

	try:
	    while not rospy.is_shutdown():
	    	alpha = (math.atan((goal_x-x)/(goal_y-y)))+math.radians(270)
	    	vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
	        if math.fabs(angulo-alpha)<0.6 or math.fabs(angulo-alpha+2*math.pi)<0.6 :
	   			if math.fabs(goal_x-x)<0.6 and math.fabs(goal_y-y)<0.6 :
					print("cheguei")
				else:
					vel = Twist(Vector3(0.4,0,0), Vector3(0,0,0))
					print("x", x)
					print("y", y)
	        else:
	        	vel = Twist(Vector3(0,0,0), Vector3(0,0,0.8))
	        	print("alpha", alpha)
	        	print("angulo", angulo)


	        velocidade_saida.publish(vel)
	        rospy.sleep(1.0)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")
