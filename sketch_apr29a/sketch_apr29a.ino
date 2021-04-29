#include <max6675.h>
#define fan 2
#define pump 4
int soPin = 8;
int csPin = 9;
int sckPin = 10;
MAX6675 robojax(sckPin, csPin, soPin);
char incomingByte; 
int temperature;   

void setup() {
  Serial.begin(9600);
  pinMode(pump, OUTPUT);
  pinMode(fan, OUTPUT);
  digitalWrite(pump, HIGH);
  digitalWrite(fan, HIGH);
}

void loop() {
  delay(1000);
  Serial.println(robojax.readCelsius());
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 'p') {
      digitalWrite(pump, !digitalRead(pump));
    }

    else if (incomingByte == 'f') {
      digitalWrite(fan, !digitalRead(fan));
    }
    
    else if (incomingByte == 'r') {
      digitalWrite(fan, HIGH);
      digitalWrite(pump, HIGH);
    }
  }
}
