
#include <Wire.h>
#include <LSM303.h>
LSM303 compass;

void setup()
{
Serial.begin(9600);
Wire.begin();
compass.init();
compass.enableDefault();
Serial.println("Magnetometer Calibrated (Units in Nanotesla)");
}

void loop()
{
compass.read();
float Xm_off, Ym_off, Zm_off, Xm_cal, Ym_cal, Zm_cal;

Xm_off = compass.m.x*(100000.0/1100.0) - 8397.862881; //X-axis combined bias (Non calibrated data - bias)
Ym_off = compass.m.y*(100000.0/1100.0) - 3307.507492; //Y-axis combined bias (Default: substracting bias)
Zm_off = compass.m.z*(100000.0/980.0 ) + 2718.831179; //Z-axis combined bias

Xm_cal =  0.949393*Xm_off + 0.006185*Ym_off + 0.015063*Zm_off; //X-axis correction for combined scale factors (Default: positive factors)
Ym_cal =  0.006185*Xm_off + 0.950124*Ym_off + 0.003084*Zm_off; //Y-axis correction for combined scale factors
Zm_cal =  0.015063*Xm_off + 0.003084*Ym_off + 0.880435*Zm_off; //Z-axis correction for combined scale factors

Serial.print(Xm_cal, 10); Serial.print(" "); Serial.print(Ym_cal, 10); Serial.print(" "); Serial.println(Zm_cal, 10);
delay(125);
}
