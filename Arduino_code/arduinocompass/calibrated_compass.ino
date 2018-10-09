
#include <ros.h>
#include <std_msgs/Float32.h>
#include <Wire.h>
#include <LSM303.h>

LSM303 compass;

ros::NodeHandle nh;
std_msgs::Float32 float_msg;
ros::Publisher chatter("/arduino/compass", &float_msg);

const float alpha = 0.15;
float fXa = 0;
float fYa = 0;
float fZa = 0;
float fXm = 0;
float fYm = 0;
float fZm = 0;

void setup() {
Serial.begin(9600);
nh.getHardware()->setBaud(9600);
nh.initNode();
nh.advertise(chatter);
Wire.begin();
compass.init();
compass.enableDefault();
}

void loop()
{
compass.read();
float pitch, pitch_print, roll, roll_print, Heading, Xa_off, Ya_off, Za_off, Xa_cal, Ya_cal, Za_cal, Xm_off, Ym_off, Zm_off, Xm_cal, Ym_cal, Zm_cal, fXm_comp, fYm_comp;

// Accelerometer calibration
Xa_off = compass.a.x/16.0 + 6.008747;
Ya_off = compass.a.y/16.0 - 18.648762;
Za_off = compass.a.z/16.0 + 10.808316;
Xa_cal =  0.980977*Xa_off + 0.001993*Ya_off - 0.004377*Za_off;
Ya_cal =  0.001993*Xa_off + 0.998259*Ya_off - 0.000417*Za_off;
Za_cal = -0.004377*Xa_off - 0.000417*Ya_off + 0.942771*Za_off;

// Magnetometer calibration
Xm_off = compass.m.x*(100000.0/1100.0) - 668.162931;
Ym_off = compass.m.y*(100000.0/1100.0) + 16592.973671;
Zm_off = compass.m.z*(100000.0/980.0 ) - 8774.227846;
Xm_cal =  0.003006*Xm_off - 0.000028*Ym_off + 0.000059*Zm_off;
Ym_cal =  -0.000028*Xm_off + 0.003020*Ym_off - 0.000028*Zm_off;
Zm_cal =  0.000059*Xm_off - 0.000028*Ym_off + 0.003199*Zm_off;

// Low-Pass filter accelerometer
fXa = Xa_cal * alpha + (fXa * (1.0 - alpha));
fYa = Ya_cal * alpha + (fYa * (1.0 - alpha));
fZa = Za_cal * alpha + (fZa * (1.0 - alpha));

// Low-Pass filter magnetometer
fXm = Xm_cal * alpha + (fXm * (1.0 - alpha));
fYm = Ym_cal * alpha + (fYm * (1.0 - alpha));
fZm = Zm_cal * alpha + (fZm * (1.0 - alpha));

// Pitch and roll
roll  = atan2(fYa, sqrt(fXa*fXa + fZa*fZa));
pitch = atan2(fXa, sqrt(fYa*fYa + fZa*fZa));
roll_print = roll*180.0/M_PI;
pitch_print = pitch*180.0/M_PI;

// Tilt compensated magnetic sensor measurements
fXm_comp = fXm*cos(pitch)+fZm*sin(pitch);
fYm_comp = fXm*sin(roll)*sin(pitch)+fYm*cos(roll)-fZm*sin(roll)*cos(pitch);

// Arctangent of y/x
Heading = (atan2(fYm_comp,fXm_comp)*180.0)/M_PI;
if (Heading < 0)
Heading += 360;

Serial.print("Pitch (X): "); Serial.print(pitch_print); Serial.print("  ");
Serial.print("Roll (Y): "); Serial.print(roll_print); Serial.print("  ");
Serial.print("Heading: "); Serial.println(Heading);
chatter.publish( &float_msg );
nh.spinOnce();
delay(250);
}
