#! /usr/bin/env python

import math
import os
import time
import signal
import serial
import sys
import xbox                     # Custom xbox module
import rospy
from std_msgs.msg import Int32MultiArray


SPEED_MULTIPLIER = 1.0          # Speed scaling factor
DIRECTION_MULTIPLIER = 0.5      # Direction scaling factor

# Protocol Data
HEADER      = 127       # Magic sync Header for the serial packet communication with the mbed
SPEED_CMD   = int(83)
CMD = 83
#MODE_CMD    = int(73)
RESET_CMD   = int(63)

# Serial port data
PORT_NAME = "/dev/ttyUSB0"
# BAUD_RATE = int(230400)
BAUD_RATE = int(115200)

serial_port = serial.Serial()           
joy         = xbox.Joystick()           # Initialize joystick

#global ultrasonic data tuple
ultrasonic_dist_arr=[]

def initSerial():
    serial_port.baudrate = BAUD_RATE
    serial_port.port     = PORT_NAME
    serial_port.open()




def packData(cmd,velocity, direction, lights):
    cmd = CMD if cmd is None else cmd
    data = bytearray()
    data.append(HEADER)
    data.append(cmd)
    data.append(velocity & 0xff)
    data.append(direction & 0xff)
    data.append(lights & 0xff)

    # for i in data:
    #     print(i)

    return data


def cleanupOnExit():
    print("-- Cleaning up and quiting!")
    #serial_port.write(packData(SPEED_CMD, int(0), int(0), int(0)))
    print("-- Mobile base stopped")

    serial_port.close()
    joy.close()
    sys.exit(0)


def waitConnect():
    # Waiting for joystick connection
    print("-- Waiting for joystick connection")
    while not joy.connected():
        time.sleep(0.01)
    print("-- Joystick connected")


def executeControls():
    needInit = False                # check for initialization
    DriveMode = True                # True: Motor drive, False: Actuator drive

    while True:
        #time.sleep(0.01)
        if not joy.connected():
            print("-- Error! Joystick disconnected - waiting for connection")
            speed       = int(0)
            direction   = int(0)

        else:
            print("Joystick Connected")  
            left_trig   = joy.leftTrigger()
            right_trig  = joy.rightTrigger()
            
            x = -joy.leftX()
            y =  joy.leftY()
            speed = 75*(right_trig) - 75*(left_trig)
            speed = speed*SPEED_MULTIPLIER
            direction = x*100
            direction = direction * DIRECTION_MULTIPLIER
            
            # Go to Actuator mode
            if joy.A() == 1 and DriveMode: 
                needInit = True
                speed = 0
                direction = 0

            # Go to Drive mode
            if joy.X() == 1 and not DriveMode: 
                needInit = True
                speed = 0
                direction = 0
        
        if speed >= 0:
            speed, direction = int(speed), -int(direction)
        else:
            speed, direction = int(speed), int(direction)
        #print("-- Speed: %d Direction: %d Drive mode: %d" % (speed, direction, DriveMode))

        cmd = CMD
        if needInit:
            #print("-- Initialisation")
            # Initialization: I-ASCII; Toggles between actuation and drive mode
            cmd = RESET_CMD 
            DriveMode = not DriveMode
            needInit = False
        
        # Soft reset of Mbed
        if joy.B() == 1:
            cmd = RESET_CMD 
            DriveMode = True
        
	    #Ultrasonic checking safe distance constraints
        safe_distance = 60
	    #print (ultrasonic_dist_arr)
        if len(ultrasonic_dist_arr)==9:
            print len(ultrasonic_dist_arr)
            #if any of the front 4 sensors on Quickie is < safe_distance, stop forward commands. 
            if (int(ultrasonic_dist_arr[1])< safe_distance and int(ultrasonic_dist_arr[1]>0)) or (int(ultrasonic_dist_arr[2])< safe_distance and int(ultrasonic_dist_arr[2]>0)) or (int(ultrasonic_dist_arr[3])< safe_distance and int(ultrasonic_dist_arr[3]>0)) or (int(ultrasonic_dist_arr[8])< safe_distance and int(ultrasonic_dist_arr[8]>0)) :
                if speed>0: 
                    speed=0
                    print "Can't move forwards."
            
            #if the back sensor on Quickie is < safe_distance, stop backward commands.     
            if (int(ultrasonic_dist_arr[7])<safe_distance) and int(ultrasonic_dist_arr[7]>0):
                if speed<0:
                    speed=0
                    print "Can't move backwards."

            #if any of the side 4 sensors on Quickie is < 30cm, stop rotation (clockwise,counterclockwise) commands.
            if (int(ultrasonic_dist_arr[0])< 30 and int(ultrasonic_dist_arr[0]>0)) or (int(ultrasonic_dist_arr[6])< 30 and int(ultrasonic_dist_arr[6]>0)) or (int(ultrasonic_dist_arr[4])< 30 and int(ultrasonic_dist_arr[4]>0)) or (int(ultrasonic_dist_arr[5])< 30 and int(ultrasonic_dist_arr[5]>0)):
                direction=0
                print "Can't move sideways."                                        
        
        #data = packData(cmd, speed, direction, int(0))
        data = packData(cmd,speed, direction, int(0))

        serial_port.write(data)


#call function to pass data to ultrasonic_dist_arr
def Get_data(data_ult):
    #print data_ult.data

     	
    global ultrasonic_dist_arr
    ultrasonic_dist_arr=(data_ult.data)
	

    


       

if (__name__ == "__main__"):
    # Handle kill commands from terminal
    signal.signal(signal.SIGTERM, cleanupOnExit)
    
    # initialize the serial port connection
    initSerial()
    
    # time.sleep(5)  # Waiting for joystick connection at the beginning
    waitConnect()
    
    	
    

    try:
        rospy.init_node('ultra_listener',anonymous='True')
        rospy.Subscriber('ultrasonic_data',Int32MultiArray,Get_data)
    
        executeControls()
            	


    except KeyboardInterrupt:
        cleanupOnExit()

                                                
                                                
    rospy.spin()                     
