#!/usr/bin/env python
import cv2
import rospy
import roslib
roslib.load_manifest('ros_vision')
from sensor_msgs.msg import Image, CameraInfo

from cv_bridge import CvBridge, CvBridgeError



def image_publisher():
    image_pub = rospy.Publisher("image_topic",Image)
    rospy.init_node('vision', anonymous=True)
    bridge = CvBridge()
    rate = rospy.Rate(10)

    dispW=1280
    dispH=720
    flip=2
    #Uncomment These next Two Line for Pi Camera
    camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 !  video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 !  appsink'
    cam= cv2.VideoCapture(camSet)

    while not rospy.is_shutdown():
        ret, frame = cam.read()
        try:
            # frame = cv2.resize(frame, (200, 200))
            image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)
        rate.sleep()

if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass