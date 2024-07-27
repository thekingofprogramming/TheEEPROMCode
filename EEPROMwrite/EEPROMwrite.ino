const int addressPins[] = {2, 3, 4, 5, 6, 7, 8, 9};  // Address pins
const int dataPins[] = {10, 11, 12, 13};             // Data pins
const int cePin = A0;                                // Chip Enable pin
const int oePin = A1;                                // Output Enable pin
const int programmingDelay = 1400;                   // EEPROM programming delay in milliseconds

void setup() {
  Serial.begin(9600);

  // Set address and data pins as outputs
  for (int i = 0; i < 8; i++) {
    pinMode(addressPins[i], OUTPUT);
  }
  for (int i = 0; i < 4; i++) {
    pinMode(dataPins[i], OUTPUT);
  }
  
  pinMode(cePin, OUTPUT);
  pinMode(oePin, OUTPUT);

  // Initialize EEPROM control pins
  digitalWrite(cePin, HIGH);
  digitalWrite(oePin, HIGH);
}

void loop() {
  if (Serial.available() >= 3) {
    byte address = Serial.read();  // Read address
    byte data = Serial.read();     // Read data
    byte command = Serial.read();  // Read command

    if (command == 0) {
      // Write command
      writeEEPROM(address, data);
    } else if (command == 1) {
      // Read command
      byte readData = readEEPROM(address);
      Serial.write(readData);  // Send the read data back
    }
  }
}

void writeEEPROM(byte address, byte data) {
  // Set address pins
  for (int i = 0; i < 8; i++) {
    digitalWrite(addressPins[i], (address >> i) & 0x01);
  }

  // Set data pins
  for (int i = 0; i < 4; i++) {
    digitalWrite(dataPins[i], (data >> i) & 0x01);
  }

  // Enable EEPROM
  digitalWrite(cePin, LOW);
  delay(programmingDelay);
  // Disable EEPROM
  digitalWrite(cePin, HIGH);
}

byte readEEPROM(byte address) {
  byte data = 0;
  
  // Set address pins
  for (int i = 0; i < 8; i++) {
    digitalWrite(addressPins[i], (address >> i) & 0x01);
  }

  // Enable EEPROM for reading
  digitalWrite(cePin, LOW);
  digitalWrite(oePin, LOW);

  // Read data pins
  for (int i = 0; i < 4; i++) {
    if (digitalRead(dataPins[i]) == HIGH) {
      data |= (1 << i);
    }
  }

  // Disable EEPROM
  digitalWrite(oePin, HIGH);
  digitalWrite(cePin, HIGH);
  
  return data;
}