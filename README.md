# Ultrasonic sensors
The Ultrasonic sensor used: [HC-SR04](https://www.sparkfun.com/products/13959)  

The line colours corresponding to the pins are as follows:  

| Colour | Pins |
| --- |---|
| Red | 5V |
| White | Gnd |
| Green | Trigger |
| Red | Echo | 

### Run Arduino code 
* In Arduino IDE, program the board with the [_ultrasonic_hcsr04.ino_](https://github.com/EE3-DTPRJ-Robot-Intelligence/Documentation-draft/blob/master/Ultrasonic/ultrasonic_hcsr04.ino) code
* Plug the pins according to the definitions in the _ultrasonic_hcsr04.ino_ code

### Gain access to port
In terminal run,  
```
sudo chmod 777 /dev/ACM0
```
### Run python directly
[ultrasonic.py](https://github.com/EE3-DTPRJ-Robot-Intelligence/Documentation-draft/blob/master/Ultrasonic/ultrasonic.py)  
In terminal run,  
```
python ultrasonic.py
```
### Run ROS
[ultrasonic_ros.py](https://github.com/EE3-DTPRJ-Robot-Intelligence/Documentation-draft/blob/master/Ultrasonic/ultrasonic_ros.py)  
In terminal run,  
```
roscore
source /devel/setup.bash
rosrun <PACKAGE NAME> ultrasonic_ros.py
```

The data (array of int) is published to this rostopic  
* /ultrasonic_data

### Notes for applying ultrasonic data (ROS) with Quickie
The idea was to utilise ultrasonic data published in rostopic and implement a safety feature on Quickie. The safety feature was to ensure that Quickie does not head in a direction where obstacles are present within 30 cm of Quickie. That means that Quickie will not respond to any command by the XBox controller which violates the 30 cm distance constraint.

In _joy_4.py_ , the constraint is set by the variable 'safe_distance' which is set to 30 cm.
The distance calculated by each ultrasonic sensor corresponds to the following indexed data of the tuple in 'ultrasonic_dist_arr'.   

Here is a diagram of the position of ultrasonic sensors on Quickie:

![](https://github.com/EE3-DTPRJ-Robot-Intelligence/Documentation-draft/blob/master/Ultrasonic/Position_of%20ultrasonic.PNG)

Bearing in mind that distances exceeding the range is set to 0, the algorithm formulated is as follows:
```python
# If ultrasonic_dist_arr[1/2/3/8] is < safe_distance and > 0,
#       If speed>0,
#             speed = 0
# If ultrasonic_dist_arr[7] is < safe_distance and > 0,
#       If speed<0,
#             speed = 0
# If ultrasonic_dist_arr[0/4/5/6] is < safe_distance and > 0,
#       direction = 0
```

### Run Quickie
In terminal run,
```
python joy_4.py
```
