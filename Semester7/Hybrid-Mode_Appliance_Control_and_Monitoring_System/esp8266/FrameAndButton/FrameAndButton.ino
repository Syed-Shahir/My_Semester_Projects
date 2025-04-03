unsigned char Buffer[8];  // Assuming the frame size is 8 bytes

void setup() {
  Serial.begin(115200); // Initialize Serial for debugging
  Serial.println("Ready to receive and display frames...");
}

void loop() {
  // Check if there's enough data for at least one frame (8 bytes)
  if (Serial.available() >= 8) {
    // Shift data until we find the start byte (0xA9)
    while (Serial.available() > 0) {
      unsigned char byte = Serial.read();
      if (byte == 0xA9) { // Start byte found
        Buffer[0] = byte;

        // Read the remaining 7 bytes of the frame
        for (int i = 1; i < 8; i++) {
          while (!Serial.available()); // Wait for each byte
          Buffer[i] = Serial.read();
        }

        // Display the aligned frame (print in hexadecimal)
        Serial.print("Aligned Frame: ");
        for (int i = 0; i < 8; i++) {
          Serial.print("0x");
          if (Buffer[i] < 0x10) Serial.print("0"); // Add leading zero for single-digit hex
          Serial.print(Buffer[i], HEX);
          Serial.print(" ");
        }
        Serial.println();

        // Identify button and state (ON/OFF)
        identifyButtonAndStatus(Buffer[3], Buffer[6]);

        break; // Exit the while loop after processing a frame
      }
    }
  }
}

// Function to identify button and ON/OFF status
void identifyButtonAndStatus(unsigned char buttonByte, unsigned char stateByte) {
  int buttonNumber;

  // Map the 4th byte to the corresponding button number
  switch (buttonByte) {
    case 0x55: buttonNumber = 1; 
    break;
    case 0xAA: buttonNumber = 2; 
    break;
    case 0x54: buttonNumber = 3; 
    break;
    case 0xEA: buttonNumber = 4; 
    break;
    default: 
      Serial.println("Unknown Button");
      return; // Exit if the button is unknown
  }

  // Determine ON/OFF state based on the 7th byte
  bool isOn = (stateByte == 0xFD); // ON if 0xFD, OFF if 0xFF

  // Print button number and status
  Serial.print("Button ");
  Serial.print(buttonNumber);
  Serial.print(" is ");
  if (isOn) {
    Serial.println("ON");
  } else {
    Serial.println("OFF");
  }
}

 