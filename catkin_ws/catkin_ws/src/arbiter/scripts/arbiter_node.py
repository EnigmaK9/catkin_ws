#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String

def arbitratorCallbackMotors1(data):
    dataMotors1[0] = data.data[0]
    dataMotors1[1] = data.data[1]
def arbitratorCallbackMotors2(data):
    dataMotors2[0] = data.data[0]
    dataMotors2[1] = data.data[1]
def alertCallback(data):
    msg_receivedCheking.data = data.data

if __name__=='__main__':
    dataMotors1 = [0.0, 0.0]
    dataMotors2 = [0.0, 0.0]
    msg_receivedPhoto = Float32MultiArray()
    msg_receivedPhoto.data = dataMotors2
    msg_receivedDodger = Float32MultiArray()
    msg_receivedDodger.data = dataMotors1
    msg_receivedCheking = String()
    rospy.init_node('Arbitrator', anonymous = True)
    ArbitratorSubs1 = rospy.Subscriber('/dodger_publisher', Float32MultiArray, arbitratorCallbackMotors1)
    ArbitratorSubs2 = rospy.Subscriber('/checking_state', String, alertCallback)
    ArbitratorSubs3 = rospy.Subscriber('/phototaxis_publisher', Float32MultiArray, arbitratorCallbackMotors2)
    ArbitratorPub = rospy.Publisher('/rotombot/hardware/motor_speeds', Float32MultiArray, queue_size = 10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        try:
            if(msg_receivedCheking.data == "false"):
                ArbitratorPub.publish(msg_receivedDodger)
            elif(msg_receivedCheking.data == "true"):
                ArbitratorPub.publish(msg_receivedPhoto)
            rate.sleep()    
            

        except rospy.ROSInterruptException:
            pass
        

    
