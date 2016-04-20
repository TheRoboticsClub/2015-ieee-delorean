
#include <Ultrasonic.h>

#define TRIGGER_PIN  1 //6 
#define ECHO_PIN     2 //7

int tx = 0; //13

Ultrasonic ultrasonic(TRIGGER_PIN, ECHO_PIN);

void setup()
  {
  Serial.begin(9600);
  pinMode(tx, OUTPUT);
  digitalWrite(tx, LOW);
  }

void loop()
  {
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();

  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);
    if(cmMsec < 5){
      digitalWrite(tx, HIGH);
    }else{
      digitalWrite(tx, LOW);
    }
    //Serial.write(int(cmMsec));
    delay(50);
  }
