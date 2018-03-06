
#include <Ultrasonic.h>

#define TRIGGER_PIN  6 //1
#define ECHO_PIN     7 //2

int tx = 13; //0

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
    if(cmMsec >= 1 && cmMsec <= 5){
      digitalWrite(tx, HIGH);
    }else{
      digitalWrite(tx, LOW);
    }
    delay(50);
  }
