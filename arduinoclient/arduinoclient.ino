#include <Wire.h>

int buzzerPin = 9;

byte sensorValue = 0; 
/* Durée du beep en ms */
int dms = 0;

void setup()
{
  pinMode(buzzerPin, OUTPUT);

  /* On configure les pins digitaux en sortie */
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  Serial.begin(9600);           // start serial for output
  
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  
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
  delay(100);
  
  if (dms > 0) {
    beep(dms);
    dms = 0;
  }
}

void receiveEvent(int howMany)
{
  unsigned char cmd = 0;
  unsigned char args[10];
  int i = 0;

  cmd = Wire.read();
  /*
   * Attention, si les données ont été envoyées par write_block_data
   * le premier argument contiendra le nombre de valeurs transmises.
   * Le premier paramètre réel sera donc dans args[1].
   */
  while (Wire.available()) {
    args[i] = Wire.read();
    i++;
  }    
  
  switch (cmd) {
    case 8: // Stockage d'une valeur pour lecture
      // Les convertisseurs sont en 10 bits (0-1023) mais
      // pour simplifier la transmission on passe en 8 bits 
      sensorValue = analogRead(args[0]) >> 2;    
      Serial.print("Read ");
      Serial.print(sensorValue);
      Serial.print(" on pin ");
      Serial.println(args[0]);
      break;
      
    case 4: // Ecriture d'une valeur analogique
      Serial.print("Write analog on pin");
      Serial.println(args[1]);
      analogWrite(args[1], args[2]);
      break;

    case 5: // Ecriture d'une valeur logique
      Serial.print("Write digital on pin ");
      Serial.println(args[1]);
      if (args[2] == 0)
        digitalWrite(args[1], LOW);
      else
        digitalWrite(args[1], HIGH);
      break;
      
    case 2: // Beep
      dms = args[0];
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

