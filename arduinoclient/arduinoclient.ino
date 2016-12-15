#include <Wire.h>

int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int buzzerPin = 9;

int sensorValue = 0; 
int dms = 0;

void setup()
{
  pinMode(buzzerPin, OUTPUT);
  
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(9600);           // start serial for output
  beep(150);
}

void beep(unsigned char delayms)
{
  analogWrite(buzzerPin, 20);
  delay(delayms);
  analogWrite(buzzerPin, 0);
  delay(delayms);  
}

void loop()
{
  delay(50);
  if (dms > 0) {
    beep(dms);
    dms = 0;
  }
}

void receiveEvent(int howMany)
{
  unsigned char cmd;
  unsigned char args[10];
  int nargs = howMany - 1;
  
  for (int i = 0; i < howMany; i++) {
    if (i == 0) {
      cmd = Wire.read();
    } else {
      args[i-1] = Wire.read();
    }
  }
  Serial.print("CMD : ");
  Serial.println(cmd);
  switch (cmd) {
    case 9: // Beep
      dms = args[0];
      break;
      
    case 8: // Stockage d'une valeur pour lecture
      if (nargs > 0)
        sensorValue = analogRead(args[0]);    
      else
        sensorValue = analogRead(sensorPin);    
      break;
      
    default:
      Serial.println("Commande inconnue");
  }
}

/*
 * Fonction appelée uniquement par la commande bus.read_byte
 * du cote Raspberry
 */
void requestEvent()
{
  Serial.println("request");
  Serial.println(sensorValue);
  Wire.write(sensorValue);
}

