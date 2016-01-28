/*
  String indexOf() and lastIndexOf() functions

 Examples of how to evaluate, look for, and replace characters in a String

 created 27 July 2010
 modified 2 Apr 2012
 by Tom Igoe

 http://www.arduino.cc/en/Tutorial/StringIndexOf

 This example code is in the public domain.
 */
 struct MyOrder{
   String Move = "";
   int Value;
 } MyOrder;
 
 String character = ".";
 

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
}

void loop() {
  // indexOf() returns the position (i.e. index) of a particular character
  // in a string. For example, if you were parsing HTML tags, you could use it:
  String stringOne = "move.50";
  int DotPos = stringOne.indexOf(character);
  Serial.println("The index of " + character + "in the string " + stringOne + " is " + DotPos);
  // Hasta aqui la funcion de buscar punto
  for(int i=0; i<DotPos; i++){
    MyOrder.Move = MyOrder.Move + stringOne[i];
   }
   Serial.println(MyOrder.Move);
  
  while (true);
}
