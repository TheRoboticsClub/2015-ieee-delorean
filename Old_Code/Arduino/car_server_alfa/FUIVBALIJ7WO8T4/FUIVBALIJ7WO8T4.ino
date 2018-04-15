#include <SoftwareServo.h> 
int potentiometer=A7;
int potval;

SoftwareServo ESC;

void setup() {
  
  pinMode(potentiometer, INPUT);
  ESC.attach(9);   
  Serial.begin(9600);    
  ESC.setMinimumPulse(800);
  ESC.setMaximumPulse(2000);
}

void loop() {

  potval=analogRead(potentiometer);
  potval=map(potval,0,1023,0,180);
  ESC.write(potval);
  SoftwareServo::refresh();
  Serial.println(potval);
 }

