/*
 * rosserial Publisher compass
 * Prints compass
 */

// Use the following line if you have a Leonardo or MKR1000 
//#define USE_USBCON 

#include <ros.h>
#include <std_msgs/Float32.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_9DOF.h>


/* Assign a ID to the compass */
Adafruit_9DOF                dof   = Adafruit_9DOF();
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);

ros::NodeHandle nh;

std_msgs::Float32 float_msg;
ros::Publisher chatter("/arduino/compass", &float_msg);

/*
 * Init sensor
 */
void initSensors()
{
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no compass detected ... Check your wiring!");
    while(1);
  }
}


void setup()
{
  Serial.begin(115200);
  Serial.println(F("We are finishing some things, please wait")); Serial.println("");
  
  /* Initialise the sensors */
  initSensors();

  /* Initialise node */
  nh.initNode();
  nh.advertise(chatter);
}

void loop()
{
  sensors_event_t mag_event;
  sensors_vec_t   orientation;
  
 /* Calculate the heading using the magnetometer */
  mag.getEvent(&mag_event);
  if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
  {
    /* 'orientation' should have valid .heading data now */
    float_msg.data = orientation.heading;
    
    chatter.publish( &float_msg );
    nh.spinOnce();
    delay(1000);
  }

}

