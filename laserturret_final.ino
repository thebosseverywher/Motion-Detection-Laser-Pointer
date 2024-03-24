#include <Servo.h>

Servo servoX;
Servo servoY;

void setup() {
  Serial.begin(9600);
  servoX.attach(9); 
  servoY.attach(10); 
}

void loop() {
  if (Serial.available() > 1) {
    
    int angleX = Serial.read();
    int angleY = Serial.read();

    servoX.write(angleX);
    servoY.write(angleY);
  }
}
