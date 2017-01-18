#include <Wire.h>

int buzzerPin = 9;

byte sensorValue = 0; 
/* Durée du beep en ms */
int dms = 0;

void setup()
{
  pinMode(buzzerPin, OUTPUT);
  
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(9600);           // start serial for output
  Serial.println("Started...");
}

void softReset()
{
  asm volatile (" jmp 0");
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
  unsigned char cmd = 0;
  unsigned char args[10];
  int nargs = howMany - 1;
  
  for (int i = 0; i < howMany; i++) {
    if (i == 0) {
      cmd = Wire.read();
    } else {
      args[i-1] = Wire.read();
    }
  }
  Serial.print("Received command ");
  Serial.print(cmd);
  Serial.print(" and ");
  Serial.print(nargs);
  Serial.println(" parameter(s)");
  
  switch (cmd) {
    case 9: // Beep
      dms = args[0];
      break;
      
    case 8: // Stockage d'une valeur pour lecture
      // Les convertisseurs sont en 10 bits (0-1023) mais
      // pour simplifier la transmission on passe en 8 bits 
      sensorValue = analogRead(args[0]) >> 2;    
      Serial.print("Read ");
      Serial.print(sensorValue);
      Serial.print(" on pin ");
      Serial.println(args[0]);
      break;
      
    case 7: // Ecriture d'une valeur
      Serial.print("Write ");
      Serial.print(args[1]);
      Serial.print(" on pin ");
      Serial.println(args[0]);
      break;
      
    case 1: 
      softReset();
      break;

    default:
      Serial.println("Unknown command");
  }
}

/*
 * Fonction appelée uniquement par la commande bus.read_byte
 * du cote Raspberry
 */
void requestEvent()
{
  Wire.write(sensorValue);
}

