#include <SimpleTimer.h>

unsigned long lastMillis;
float vel;
float deltaMillis;
float lastSensorUpdate;

SimpleTimer timer;


void setup() {
  deltaMillis = 1000000.0;
  lastMillis = millis();
  lastSensorUpdate = millis();
  vel = 0.00;
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), sensor, FALLING);

}

void loop() {

  checkSensorUpdate();
  Serial.print(vel);
  Serial.println(" meters/second");
  delay(500);

}

void checkSensorUpdate(){
  if(millis()- lastSensorUpdate >= 5000){
    //Serial.println("Car is stopped");
    vel = 0.00;
  }
}


void sensor(){
  
  deltaMillis = millis()- lastMillis; //This is the time that passed between sensor activation (magnet passing)
  vel = (0.3760/(deltaMillis/1000)); //speed of the car
  //Serial.print(vel);
  //Serial.println(" meters/second");
  lastMillis = millis();
  lastSensorUpdate = millis();
}

