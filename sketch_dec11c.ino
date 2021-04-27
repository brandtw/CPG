#include <max6675.h>

int soPin = 8;// SO=Serial Out
int csPin = 9;// CS = chip select CS pin
int sckPin = 10;// SCK = Serial Clock pin

MAX6675 robojax(sckPin, csPin, soPin);// create instance object of MAX6675

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(4,OUTPUT);
  pinMode(2,OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(4, HIGH);
  digitalWrite(2, HIGH);
  //delay(1000);
  //digitalWrite(4, LOW);
  //digitalWrite(2, LOW);
  Serial.print("C = "); 
  Serial.print(robojax.readCelsius());
  Serial.print(" F = ");
  Serial.println(robojax.readFahrenheit());

             
   delay(1000);
}
