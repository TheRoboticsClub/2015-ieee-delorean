//Código implementado para Arduino uno
#include <Arduino.h>
#include <NewPing.h>

const int ledPIN = 3;
const int MaxDistance = 200;
const int SONAR_NUM = 3;      // Number of sensors.
/*Hagamos un array de ultrasonidos */
NewPing sonar[SONAR_NUM] = {   // Sensor object array.
  NewPing(12, 13, MaxDistance), // Each sensor's trigger pin, echo pin, and max distance to ping.
  NewPing(10, 9, MaxDistance),
  NewPing(6, 5, MaxDistance)
};


void setup() {
  Serial.begin(9600);
pinMode(ledPIN , OUTPUT);
}
void loop() {
    /*digitalWrite(ledPIN , LOW);*/

  for (int i = 0; i < SONAR_NUM; i++) { // Loop through each sensor and display results.
    delay(100); // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
    Serial.print(i);
    Serial.print("=");
    Serial.print(sonar[i].ping_cm());
    if (sonar[0].ping_cm()<15 || sonar[1].ping_cm()<15 || sonar[2].ping_cm()<15){
        Serial.println("Me meto pa encender el led");
        if(sonar[0].ping_cm()>1 || sonar[1].ping_cm()>1 || sonar[2].ping_cm()>1){
            //Esta condición es para cuando el sensor está mirando al infinito va a devolver un 0 por loq ue se debec ontrloar esa excepción.
            digitalWrite(ledPIN , HIGH);
        }
        delay(100);
    }else{
        digitalWrite(ledPIN , LOW);
        delay(100);
    }
    Serial.print("cm ");
  }
  Serial.println();
}
