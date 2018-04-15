
#include <Servo.h>
#define neutralThrottle 1500
#define neutralSteering 90

Servo ESC;
Servo steering;

void setup() {
  ESC.attach(5);
  steering.attach(3);
  Serial.begin(9600);
  Serial.setTimeout(50);

}

void loop() {

  int myOrder = 3000;

  
   while(Serial.available()){
      myOrder = Serial.parseInt();     //this reads strings from the serial ports and store them in to the variable
   }

   if(myOrder >= 1000 && myOrder <= 2000){
    ESC.writeMicroseconds(myOrder);
    Serial.print("I am activating the ESC. Speed: ");
    Serial.println(myOrder);
   }

   if(myOrder >= 0 && myOrder <= 180){
    steering.write(myOrder);
    Serial.print("I am steering to: ");
    Serial.println(myOrder);
   }

}
