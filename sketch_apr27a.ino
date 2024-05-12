#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Initialise l'afficheur LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);
const int ledPin2 = 2;  
const int ledPin3 = 3;

void setup() {
  lcd.init(); // Démarre l'afficheur
  lcd.backlight(); // Allume le rétro-éclairage
  lcd.print("waiting ....."); // Affiche "Hello, World!" sur le premier ligne
  pinMode(ledPin2, OUTPUT); // pin D2 in arduino mode mte3ha output to send signal (courant)
  pinMode(ledPin3, OUTPUT); // pin D3 in arduino mode mte3ha output to send signal (courant)
  Serial.begin(9600); // the pc and arduino will use same frequence to talk with each other
}

void loop() {
  digitalWrite(ledPin3, LOW); // turn off led 1 man3adiwich courant in pin
  digitalWrite(ledPin2, LOW); // Turn off LED 2 man3adiwich courant in pin

  if (Serial.available() > 0) { // Check if serial data is available (idhakan da5alna haja f serial monitor)
    char input = Serial.read(); // Read the incoming byte yili ktibto
    
    if (input == '1') { // If '1' is received, turn on green
      digitalWrite(ledPin3, LOW); // low man3adiwich courant in red led
      digitalWrite(ledPin2, HIGH); // Turn on LED 3 (green)
      lcd.clear();
      lcd.print("Access Granted");
      delay(285); // wait 0.5 seconds
    } if (input == '0') { // For any other input, turn on red
      digitalWrite(ledPin2, LOW); // Turn off green 
      digitalWrite(ledPin3, HIGH); // Turn on red
      delay(285); 
      lcd.clear();
      lcd.print("Access Denied");
    }
    else {
        digitalWrite(ledPin3, LOW); // Turn off red
        digitalWrite(ledPin2, LOW); // Turn off green
    }
  }
}