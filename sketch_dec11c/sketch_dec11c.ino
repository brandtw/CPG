#include <max6675.h>

int soPin = 8;
int csPin = 9;
int sckPin = 10;
MAX6675 robojax(sckPin, csPin, soPin);
String incomingByte;    

void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(4, HIGH);
  digitalWrite(2, HIGH);
}

void loop() {
  if (Serial.available() > 0) {
  incomingByte = Serial.readStringUntil('\n');
    if (incomingByte == "pump on") {
      digitalWrite(4, LOW);
      Serial.write("Pump on");
    }

    else if (incomingByte == "pump off") {
      digitalWrite(4, HIGH);
      Serial.write("Pump off");
    }

    else if (incomingByte == "fan off") {
      digitalWrite(2, HIGH);
      Serial.write("Fan off");
    }

    else if (incomingByte == "fan on") {
      digitalWrite(2, LOW);
      Serial.write("Fan on");
    }

    else if (incomingByte == "temp") {
      Serial.print(" C = ");
      Serial.print(robojax.readCelsius());
      Serial.print(" F = ");
      Serial.println(robojax.readFahrenheit());
    }

    else{
     Serial.write("invald input");
    }
  }
}
