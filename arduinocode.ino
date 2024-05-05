#include <Keypad.h>

const byte ROWS = 4; 
const byte COLS = 4; 

byte rowPins[ROWS] = {22, 23, 24, 25}; 
byte colPins[COLS] = {26, 27, 28, 29}; 

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

const String correctPasscode = "1234";
String enteredPasscode = "";
int remainingAttempts = 5;

int redPin = 44;    
int greenPin = 45;  
int bluePin = 47;  
int buzzerPin = 53; 

const int trigPin = 50; 
const int echoPin = 51; 

bool applicationRunning = true;
bool sensorRunning = true; 

void setup() {
  Serial.begin(9600);

  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int alarmCheck = Serial.parseInt();
    if (alarmCheck == 1) {
      // Face and voice recognition successful
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      tone(buzzerPin, 1000);
      delay(1000);
      noTone(buzzerPin);
      digitalWrite(greenPin, LOW);
      delay(1000);
      applicationRunning = false;
    } else if (alarmCheck == 0) {
      // Face or voice recognition failed
      // Handle accordingly
    }
    
    // Flush the serial buffer to clear any remaining data
    Serial.flush();
  }

  if (applicationRunning) {
    char key = keypad.getKey();

    if (key != NO_KEY) {
      digitalWrite(buzzerPin, HIGH); 
      delay(50); 
      digitalWrite(buzzerPin, LOW); 
      if (key != '#') {
        enteredPasscode += key;
      } else {
        if (enteredPasscode == correctPasscode) {
          // Perform successful authentication actions
          digitalWrite(greenPin, HIGH);
          digitalWrite(redPin, LOW);
          tone(buzzerPin, 1000);
          delay(1000);
          noTone(buzzerPin);
          digitalWrite(greenPin, LOW);
          delay(1000);
          applicationRunning = false;
        } else {
          // Perform unsuccessful authentication actions
          remainingAttempts--;
          digitalWrite(redPin, HIGH);
          tone(buzzerPin, 500);
          delay(1000);
          noTone(buzzerPin);
          if (remainingAttempts == 0) {
            digitalWrite(redPin, HIGH);
            while (true) {
              digitalWrite(buzzerPin, HIGH);
              delay(500);
              digitalWrite(buzzerPin, LOW);
              digitalWrite(redPin, HIGH);
              delay(500);
              digitalWrite(redPin, LOW);
              delay(500);
            }
          }
        }
        enteredPasscode = "";
      }
    }
  }

  if (sensorRunning) { // 
    long duration, distance;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2; 
    digitalWrite(bluePin, HIGH);

    if (distance < 10) {
      sensorRunning = false;
      digitalWrite(bluePin, LOW);
    
      for (int i = 0; i < 5; i++) {
        digitalWrite(buzzerPin, HIGH); 
        delay(500); 
        digitalWrite(buzzerPin, LOW); 
        delay(500); 
      }
    }
  } else { 
    char key = keypad.getKey();

    if (key != NO_KEY) {
    }
  }
}
