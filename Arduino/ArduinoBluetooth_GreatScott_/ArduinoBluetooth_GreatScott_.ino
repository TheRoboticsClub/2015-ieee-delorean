//http://www.youtube.com/user/greatscottlab
#include <Servo.h> //Librera para controlar los servos
Servo servogiro;
Servo variador;

int motorpin = 5;
//int pos = 0;
int ledred=12;
int tx=1;
int rx=0;
char inSerial[15];
//int sensormov;
int datreceptor = A1;
int angulo = 90; // Con esto centro la direccin desde el principio
int go =1500; //No hay variacin de velocidad

void setup(){ 
  //aqui declaramos los conectores del Arduino
  
  Serial.begin(9600);
  pinMode(ledred, OUTPUT);
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
    delay(500);                                         
    if (Serial.available() > 0) {             
       while (Serial.available() > 0) {
         inSerial[i]=Serial.read(); 
         i++;      
       }
       inSerial[i]='\0';
      Check_Protocol(inSerial);
     }} 
 
void Check_Protocol(char inStr[]){   
  int i=0;
  int m=0;
  Serial.println(inStr);
  
    if(!strcmp(inStr,"r")){
      angulo+=45; // derecha 45 grados
      for(m=0;m<11;m++){
        inStr[m]=0;}
         i=0;}
         
    if(!strcmp(inStr,"l")){
      angulo-=45; //izquierda 45 grados
      for(m=0;m<11;m++){
        inStr[m]=0;}
         i=0;}
    
    angulo=constrain(angulo,0,180); //con esto decimos que el ngulo va de 0-180    
    servogiro.write(angulo);              // tell servo to go to position in variable 'pos' 
           
    if(!strcmp(inStr,"move")){     //Manejo del variador
      // en esta condición manejamos el variador
      Serial.println("motors on");
        go= go + 10;
      
      for(m=0;m<11;m++){
          inStr[m]=0;}
            i=0;}   
      variador.writeMicroseconds(go);

    if(!strcmp(inStr,"stop")){ //parada de emergencia
    
      go =1500;
            variador.writeMicroseconds(go);

    for(m=0;m<11;m++){
        inStr[m]=0;}
         i=0;}
         
        
    else{
    for(m=0;m<11;m++){
      inStr[m]=0;
    }
    i=0;
}}
  
