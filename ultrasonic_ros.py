#!/usr/bin/env python

#Getting data from arduino, ultrasonic sensors in array format for processing
import serial
import rospy
import matplotlib.pyplot as plt
from std_msgs.msg import Int32MultiArray
import time

def main():
	ser=serial.Serial('/dev/ttyACM0',9600)
	#ros init node
	pub = rospy.Publisher('ultrasonic_data',Int32MultiArray,queue_size=20)
	rospy.init_node('sender',anonymous=True)
	r = rospy.Rate(100)
	start_time=time.time()
	count_time=start_time
	c=0    #counter	
	while not rospy.is_shutdown():
		line=ser.readline()
		if (line[0]=='S' and line[-1]=='\n'):        #if first bit is start bit ('S'), valid data stream 
			#print ('serial data:'+line)
			a1=[]    #data in array format
			buf=''	 #buffer to reconstruct data values from characters 
			for i in line[1:]:
        			if i=='\n':
					a1.append(int(buf))
             				break
        			else:
                			if (i==','):
                        			a1.append(int(buf))
                        			buf=''
                			else:
              		          		if i in ['0','1','2','3','4','5','6','7','8','9'] :
							buf+=i
						else:
							print 'Invalid char'
							a1=[]
							break
 			print (a1)
			a=Int32MultiArray()
			a.data=a1
			pub.publish(a)
			if len(a1)==9 and (time.time()-count_time)>0.5:
				count_time=time.time()
				plt.plot(time.time()-start_time,a1[0],'rx')
				plt.plot(time.time()-start_time,a1[1],'kx')
				plt.plot(time.time()-start_time,a1[2],'yx')
				plt.plot(time.time()-start_time,a1[3],'bx')
				plt.plot(time.time()-start_time,a1[4],'gx')
				plt.plot(time.time()-start_time,a1[5],'mx')
				plt.plot(time.time()-start_time,a1[6],'wx')
				plt.plot(time.time()-start_time,a1[7],'cx')
				plt.plot(time.time()-start_time,a1[8],'^')
				plt.draw()
				
				plt.pause(0.000001)
				if c==40:
					plt.clf()
					c=0
				else:
					c+=1
		else:
			print 'Not start bit.'    #else if incomplete data stream, wait till next complete data stream and print message.
			print '>>'+line
			line=''
		r.sleep()
		
		
if __name__=='__main__':
	main()
