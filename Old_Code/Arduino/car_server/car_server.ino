//http://www.youtube.com/user/greatscottlab
#include <Servo.h> //Librera para controlar los servos
#include <CreateType.h>

Servo servogiro;
Servo variador;
CreateType CT;

CreateType::Order MyOrder;
int motorpin = 5;
//int pos = 0;
int tx=1;
int rx=0;
//char inSerial[15];
String inSerial = "";
//int sensormov;
int datreceptor = A1;
int angulo = 90; // Con esto centro la direccin desde el principio
int go =1500; //No hay variacin de velocidad

void setup(){ 
  //aqui declaramos los conectores del Arduino
  
  Serial.begin(9600);
  pinMode(tx, OUTPUT);
  pinMode(rx, INPUT);
  pinMode(datreceptor,INPUT);
  
  servogiro.attach(3);
  variador.attach(motorpin);
  
}

void loop(){
    analogWrite(motorpin, 0);
    int i=0;
    int m=0;
    inSerial = "";
    delay(500);                                         
    if (Serial.available() > 0) {             
       while (Serial.available() > 0) {
         inSerial= inSerial + char(Serial.read());       
       }
      // inSerial[i]='\0';
      Check_Protocol(inSerial);
     }} 
 
void Check_Protocol(String inStr){   
  int i=0;
  int m=0;
  
  
  MyOrder.Move = "";
  MyOrder.Value = 0;
  MyOrder = CT.AddMyType(inStr);
  
  //Serial.println(MyOrder.Move);
  //Serial.println(MyOrder.Value);
    
    if(MyOrder.Move == "turn"){
      Serial.print("Turn ");
      Serial.print(MyOrder.Value);
      Serial.println(" degrees");

      angulo=MyOrder.Value; // Use of rotations
      inStr="";             // Reset inStr 
    }
    
    angulo=constrain(angulo,45,135); //con esto decimos que el angulo va de 0-180    
    servogiro.write(angulo);              // tell servo to go to position in variable 'pos' 
           
    if(MyOrder.Move == "move"){     //Manejo del variador
      // en esta condición manejamos el variador
      go = 1500 + MyOrder.Value;
      Serial.print("Speed: ");
      Serial.println(go);
      inStr = "";
         
      variador.writeMicroseconds(go);
    }
    if(MyOrder.Move == "stop"){ //parada de emergencia
      Serial.println("Stopped");
      go = 1500;
      variador.writeMicroseconds(go);
      inStr = "";
      
    }        
    else{
    inStr = "";
    }
  }  
