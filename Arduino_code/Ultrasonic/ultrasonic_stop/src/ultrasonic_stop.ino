#include <Arduino.h>
#include <NewPing.h>


const int UltrasonicPin = 6;
const int ECHO_PIN = 5;
const int MaxDistance = 200;

NewPing sonar(UltrasonicPin, ECHO_PIN, MaxDistance);
/*Hagamos un array de ultrasonidos */


void setup() {
  Serial.begin(9600);
}
void loop() {
  delay(100);
  Serial.print("Ping: ");                      // esperar 50ms entre pings (29ms como minimo)
  Serial.print(sonar.ping_cm()); // obtener el valor en cm (0 = fuera de rango)
  Serial.println("cm");
}
