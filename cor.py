#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import tf
import math
import cv2
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

cv_image = None

def processa(dado):
	frame = dado
	frame_r = frame[:,:,2]
	frame_g = frame[:,:,1]
	frame_rg = cv2.subtract(frame_r, frame_g)

	ret, frame_rg = cv2.threshold(frame_rg, 40, 255, cv2.THRESH_BINARY)

	x_m = 0
	y_m = 0
	total = 0
	media = []

	for i in range(frame_rg.shape[0]):
	    for j in range(frame_rg.shape[1]):
	        if frame_rg[i][j] == 255:
	            x_m = x_m+i
	            y_m = y_m+j
	            total += 1

	media = [x_m/total, y_m/total]
	cv2.circle(frame_rg, tuple(media), 10, (128,128,0))
	cv2.imshow("caixa",frame_rg)
	cv2.waitKey(1)
	print(media)
	return (media)

def recebe(imagem):
	global cv_image
	try:
		print("img recebida")
		cv_image = bridge.imgmsg_to_cv2(imagem, "bgr8")
		cv2.imshow("video", cv_image)
		cv2.waitKey(1)
		processa(cv_image)
	except CvBridgeError as e:
		print(e)


if __name__=="__main__":

	rospy.init_node("cor")
	recebedor = rospy.Subscriber("/camera/image_raw", Image, recebe)

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )

	cv2.namedWindow("caixa")
	cv2.namedWindow("video")

	try:

		while not rospy.is_shutdown():
	   #  	alpha = (math.atan((goal_x-x)/(goal_y-y)))+math.radians(270)
	   #  	vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
	   #      if math.fabs(angulo-alpha)<0.6 or math.fabs(angulo-alpha+2*math.pi)<0.6 :
	   # 			if math.fabs(goal_x-x)<0.6 and math.fabs(goal_y-y)<0.6 :
				# 	print("cheguei")
				# else:
				# 	vel = Twist(Vector3(0.4,0,0), Vector3(0,0,0))
				# 	print("x", x)
				# 	print("y", y)
	   #      else:
	   #      	vel = Twist(Vector3(0,0,0), Vector3(0,0,0.8))
	   #      	print("alpha", alpha)
	   #      	print("angulo", angulo)


	   #      velocidade_saida.publish(vel)
			rospy.sleep(1.0)
			print("OI")

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")


