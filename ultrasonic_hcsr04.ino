
#define trigPin1 2
#define echoPin1 3
#define trigPin2 4
#define echoPin2 5
#define trigPin3 6
#define echoPin3 7
#define trigPin4 8
#define echoPin4 9
#define trigPin5 10
#define echoPin5 11
#define trigPin6 12
#define echoPin6 13
#define trigPin7 A0
#define echoPin7 A1
#define trigPin8 A2
#define echoPin8 A3
#define trigPin9 A4
#define echoPin9 A5
long  duration,  distance,  FrontSensor1,  FrontSensor2,  FrontSensor3,  FrontSensor4, RightSensor1, RightSensor2, LeftSensor1, LeftSensor2, BackSensor;

int timeout_pulseIn=25000;        //PulseIn timeout period, default 25000 
char buff[10];                //10 bytes to store maximum of 10 chars
void setup(){
    Serial.begin (9600);
    pinMode(trigPin1, OUTPUT);
    pinMode(echoPin1, INPUT);
    pinMode(trigPin2, OUTPUT);
    pinMode(echoPin2, INPUT);
    pinMode(trigPin3, OUTPUT);
    pinMode(echoPin3, INPUT);
    pinMode(trigPin4, OUTPUT);
    pinMode(echoPin4, INPUT);
    pinMode(trigPin5, OUTPUT);
    pinMode(echoPin5, INPUT);
    pinMode(trigPin6, OUTPUT);
    pinMode(echoPin6,INPUT);
    pinMode(trigPin7, OUTPUT);
    pinMode(echoPin7, INPUT);
    pinMode(trigPin8, OUTPUT);
    pinMode(echoPin8, INPUT);
    pinMode(trigPin9, OUTPUT);
    pinMode(echoPin9, INPUT);
    }
    
void loop() {
  FrontSensor1 = SonarSensor(trigPin1, echoPin1);
  FrontSensor2 = SonarSensor(trigPin2, echoPin2);
  FrontSensor3 = SonarSensor(trigPin3, echoPin3);
  FrontSensor4 = SonarSensor(trigPin4, echoPin4);
  RightSensor1 = SonarSensor(trigPin5, echoPin5);
  RightSensor2 = SonarSensor(trigPin6, echoPin6);
  LeftSensor1 = SonarSensor(trigPin7, echoPin7);
  LeftSensor2 = SonarSensor(trigPin8, echoPin8);
  BackSensor = SonarSensor(trigPin9, echoPin9);

 /* if (Serial.available()>0){
    Serial.readBytes(buff,10);   //read timeout period from user
    
    
    
  }
  timeout_pulseIn =atoi(buff);*/
  //Serial.print(char(timeout_pulseIn));
  //Serial.print((timeout_pulseIn));
  Serial.print('S');
  Serial.print(LeftSensor1);
  Serial.print(',');
  Serial.print(LeftSensor2);
  Serial.print(',');
  Serial.print(FrontSensor1);
  Serial.print(',');
  Serial.print(FrontSensor2);
  Serial.print(',');
  Serial.print(FrontSensor3);
  Serial.print(',');
  Serial.print(FrontSensor4);
  Serial.print(',');
  Serial.print(RightSensor1);
  Serial.print(',');
  Serial.print(RightSensor2);
  Serial.print(',');
  Serial.print(BackSensor);
  Serial.print('\n');
  }
  
int SonarSensor(int trigPin,int echoPin){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);/* Ensure the trigPin stays low initially */
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW); /* Transmit the ultrasonic pulse for 10ms */
  duration = pulseIn(echoPin, HIGH,timeout_pulseIn);/* The time in microseconds for the echoPin to receive the reflected 
  ultrasonic pulse from the obstacle after pulse transmitted from trigPin. The timeout is in microseconds
  (default (i.e. no number specified) timeout is 1 second) */
  distance  =  (duration*0.0172);  /*  (duration*0.5*0.034)Time  divided  by  two  because  it  covers  double distance;Division of 29.1; Distance calculated from duration times speed of sound */
  if (distance>400 ){
    distance=0;
    
  }
  return distance;
  }


//send serial.print to text file
//cat /dev/ttyACM0 > ard_data_ultrasonic.txt
