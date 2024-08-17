#include <Servo.h>

String cmd;
String lastCmd = "";  // To store the last executed command

Servo myservo1;       // Index
Servo myservo2;       // Thumb
Servo myservo3;       // Middle
Servo myservo4;       // Ring
Servo myservo5;       // Pinky

int servoIndex = 12;
int servoThumb = 13;
int servoMiddle = 11;
int servoRing = 10;
int servoPinky = 9;

int redLEDPin = 7;    // Red LED pin for loss
int greenLEDPin = 4;  // Green LED pin for win

int pos = 0;  
int dt = 2;

void Rock() {
  for (pos = 0; pos <= 180; pos += 1) {
    myservo1.write(pos);
    myservo2.write(pos);
    myservo3.write(pos);  
    myservo4.write(pos);
    myservo5.write(pos);
    delay(dt);  
  }

  delay(20);

  // Move servos back to 0 degrees
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo1.write(pos);
    myservo2.write(pos);
    myservo3.write(pos);  
    myservo4.write(pos);
    myservo5.write(pos); 
    delay(4);  
  }
}

void Paper() {
  myservo1.write(0);  
  myservo2.write(0);
  myservo3.write(0); 
  myservo4.write(0);
  myservo5.write(0);
}

void Scissors() {
  for (pos = 0; pos <= 180; pos += 1) {
    myservo2.write(pos);
    myservo4.write(pos);
    myservo5.write(pos);
    delay(4);  
  }

  delay(20);

  // Move servos back to 0 degrees
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo2.write(pos);
    myservo4.write(pos);
    myservo5.write(pos);
    delay(4);  
  }
}

void setup() {
  myservo1.attach(servoIndex); 
  myservo2.attach(servoThumb); 
  myservo3.attach(servoMiddle); 
  myservo4.attach(servoRing); 
  myservo5.attach(servoPinky); 
  
  // Set initial position to 0 degrees
  myservo1.write(0);  
  myservo2.write(0);
  myservo3.write(0); 
  myservo4.write(0);
  myservo5.write(0);

  pinMode(redLEDPin, OUTPUT);
  pinMode(greenLEDPin, OUTPUT);
  
  delay(1000);  // Optional: give some initial time delay if needed
  Serial.begin(115200);
}

void loop() {
   if (Serial.available() > 0) {
    cmd = Serial.readStringUntil('\r'); // Read until carriage return
    
    // Only execute if the command is different from the last one
    if (cmd != lastCmd) {
      digitalWrite(redLEDPin, LOW);
      digitalWrite(greenLEDPin, LOW);

      Serial.println(cmd); // For debugging, see what command is received

      if (cmd.indexOf("Computer: Rock") >= 0) {
        Rock();
      } 
      else if (cmd.indexOf("Computer: Paper") >= 0) {
        Paper();
      } 
      else if (cmd.indexOf("Computer: Scissors") >= 0) {
        Scissors();
      }
      else if (cmd.indexOf("Computer: Unknown") >= 0) {
        Paper();  // Default to Paper if Unknown
      }

      // Determine if the player won or lost
      if (cmd.indexOf("Player: Won") >= 0) {
        digitalWrite(greenLEDPin, HIGH);  // Light up green LED
      } 
      else if (cmd.indexOf("Player: Lost") >= 0) {
        digitalWrite(redLEDPin, HIGH);  // Light up red LED
      }
      else if (cmd.indexOf("It's a Tie") >= 0) {
        digitalWrite(redLEDPin, HIGH);  // Light up red LED
        digitalWrite(greenLEDPin, HIGH);  // Light up green LED
      }
      else if (cmd.indexOf("Unknown") >= 0) {
        digitalWrite(redLEDPin, LOW);  // Turn off LEDs if Unknown
        digitalWrite(greenLEDPin, LOW);
      }
      lastCmd = cmd;  // Store the last command
    }
  }
}
