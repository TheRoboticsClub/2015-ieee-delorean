/*
 Primeras pruebas para identificar los mensajes que le llgan al bluetooth

 */

 //Con struct, creamos nuestro tipo 
 struct MyOrder{
   String Move = "";
   int Value= 0;
 } MyOrder;
 // Aquí definimos el tipo de caracter que queremos buscar
 //Lo hemos hecho con una variable por si en un futuro necesitamos
 // más está función
 String character = ".";
 

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
}

void loop() {
  // indexOf() returns the position (i.e. index) of a particular character
  // in a string. For example, if you were parsing HTML tags, you could use it:

  String stringOne = "move.100";
  String AuxValuechar;

  int DotPos = stringOne.indexOf(character);
  Serial.println("The index of " + character + "in the string " + stringOne + " is " + DotPos);

  // Hasta aqui la funcion de buscar punto
  //Futura función para meter las órdenes y valores en nuestro tipo
  for(int i=0; i<DotPos; i++){
    MyOrder.Move = MyOrder.Move + stringOne[i];
   }
   Serial.println(MyOrder.Move);

   for(int i=DotPos+1; i<stringOne.length(); i++){
        AuxValuechar = AuxValuechar + stringOne[i];
   }
    MyOrder.Value = AuxValuechar.toInt();

    Serial.println(MyOrder.Value);
    //Serial.println(MyOrder);
  
  while (true);
}
