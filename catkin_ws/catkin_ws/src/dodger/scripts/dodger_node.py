#!/usr/bin/env python

import rospy
import numpy
from collections import deque
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String

s1q = deque([0,0,0,0,0])
s2q = deque([0,0,0,0,0])
s3q = deque([0,0,0,0,0])
s4q = deque([0,0,0,0,0])
s5q = deque([0,0,0,0,0])
s6q = deque([0,0,0,0,0])
s7q = deque([0,0,0,0,0])
s8q = deque([0,0,0,0,0])



def dodgerCallback(sonicData):
    
    """obstacle[0] = sonicData.data[5] #sensor 2
    obstacle[1] = sonicData.data[6] #sensor 3
    obstacle[2] = sonicData.data[7] #sensor 4
    obstacle[3] = sonicData.data[1] #sensor 6
    obstacle[4] = sonicData.data[2] #sensor 7
    obstacle[5] = sonicData.data[3] #sensor 8
    obstacle[6] = sonicData.data[4] #sensor 1
    obstacle[7] = sonicData.data[0] #sensor 5"""
    s1q.popleft()
    s2q.popleft()
    s3q.popleft()
    s4q.popleft()
    s5q.popleft()
    s6q.popleft()
    s7q.popleft()
    s8q.popleft()
    s1q.append(sonicData.data[0])
    s2q.append(sonicData.data[1])
    s3q.append(sonicData.data[2])
    s4q.append(sonicData.data[3])
    s5q.append(sonicData.data[4])
    s6q.append(sonicData.data[5])
    s7q.append(sonicData.data[6])
    s8q.append(sonicData.data[7])

if __name__=='__main__':
    
    msgChecking = String()
    obstacle = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    motors = [0.0, 0.0]
    umbral = 0.25
    count = 20
    counterfront = 0
    counterback = 0
    countleft = 0
    countright = 0
    msgsDirection = Float32MultiArray()
    msgsDirection.data = motors
    rospy.init_node('dodger', anonymous = True)
    dodgerPub1 = rospy.Publisher('dodger_publisher', Float32MultiArray, queue_size = 10)
    dodgerPub2 = rospy.Publisher('Checking_state', String, queue_size = 10)
    dodgerSub = rospy.Subscriber('/rotombot/hardware/distance_sensors', Float32MultiArray, dodgerCallback)
    rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        obstacle[7] = numpy.mean(s1q)
        obstacle[3] = numpy.mean(s2q)
        obstacle[4] = numpy.mean(s3q)
        obstacle[5] = numpy.mean(s4q)
        obstacle[6] = numpy.mean(s5q)
        obstacle[0] = numpy.mean(s6q)
        obstacle[1] = numpy.mean(s7q)
        obstacle[2] = numpy.mean(s8q)

        msgChecking.data = "true"
   
        try:
            for i in range(count):
                if obstacle[0] < umbral or obstacle[2] < umbral:
                    countleft += 1
                elif obstacle[3] < umbral or obstacle[5] < umbral:
                    countright += 1
                elif obstacle[6] < umbral:
                    counterfront += 1
                elif obstacle[7] < umbral:
                    counterback += 1   
               
            if countleft >= count and countright < count and counterfront < count and counterback < count:
                motors[0] = 0.80
                motors[1] = -0.80
                msgChecking.data = "false"
            elif countright >= count and countleft < count and counterfront < count and counterback < count:
                motors[0] = -0.80
                motors[1] = 0.80
                msgChecking.data = "false"
            elif counterfront >= count and countright < count and countleft < count and counterback < count:
                motors[0] = -0.6
                motors[1] = -0.6
                msgChecking.data = "false"
           
            

            countleft = 0
            countright = 0  
            counterfront = 0
            counterback = 0          
            dodgerPub1.publish(msgsDirection)
            dodgerPub2.publish(msgChecking)
            rate.sleep()

        except rospy.ROSInterruptException:
            pass
            
        

