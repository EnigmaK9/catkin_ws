#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

def photocallback(sensors):
    motorwheels[0] = sensors.data[0] #sensor derecho
    motorwheels[1] = sensors.data[1] # sensor izquierdo

#Main Function/////////////////////////////////////////////////////////////////
if __name__=='__main__':
    motorwheels = [0.0, 0.0]
    motors = [0.0, 0.0]
    msgsMotors = Float32MultiArray()
    msgsMotors.data = motors
    rospy.init_node('phototaxis', anonymous = True)
    photoPub = rospy.Publisher('phototaxis_publisher', Float32MultiArray, queue_size = 10)
    photoSub = rospy.Subscriber('/rotombot/hardware/arduino_sensors', Float32MultiArray, photocallback)
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        try:
            if (motorwheels[1] - motorwheels[0] > 0.0 and motorwheels[1] - motorwheels[0] < 0.1) or (motorwheels[0] - motorwheels[1] > 0.0 and motorwheels[0] - motorwheels[1] < 0.1):
                motors[0] = 0.5
                motors[1] = 0.5
            elif motorwheels[1] - motorwheels[0] > 0.1:
                motors[0] = 0.75
                motors[1] = -0.75
            elif motorwheels[0] - motorwheels[1] > 0.1:
                motors[0] = -0.75
                motors[1] = 0.75

            photoPub.publish(msgsMotors)
            rate.sleep()
        except rospy.ROSInterruptException:
            pass
            
       
    
#///////////////////////////////////////////////////////////////////////////////
