unsigned char Buffer[8];  // Assuming the frame size is 8 bytes

// Define the GPIO pins for buttons
#define BUTTON1_PIN D0
#define BUTTON2_PIN D1
#define BUTTON3_PIN D2
#define BUTTON4_PIN D3

void setup() {
  Serial.begin(115200); // Initialize Serial for debugging
  Serial.println("Ready to receive and display frames...");
  
  // Initialize GPIO pins as output
  pinMode(BUTTON1_PIN, OUTPUT);
  pinMode(BUTTON2_PIN, OUTPUT);
  pinMode(BUTTON3_PIN, OUTPUT);
  pinMode(BUTTON4_PIN, OUTPUT);

  // Set all pins to LOW initially
  digitalWrite(BUTTON1_PIN, LOW);
  digitalWrite(BUTTON2_PIN, LOW);
  digitalWrite(BUTTON3_PIN, LOW);
  digitalWrite(BUTTON4_PIN, LOW);
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
        identifyButtonAndControlPins(Buffer[3], Buffer[6]);

        break; // Exit the while loop after processing a frame
      }
    }
  }
}

// Function to identify button and control GPIO pins
void identifyButtonAndControlPins(unsigned char buttonByte, unsigned char stateByte) {
  int buttonNumber;
  int pinToControl;

  // Map the 4th byte to the corresponding button number and pin
  switch (buttonByte) {
    case 0x55: 
      buttonNumber = 1;
      pinToControl = BUTTON1_PIN;
      break;
    case 0xAA: 
      buttonNumber = 2;
      pinToControl = BUTTON2_PIN;
      break;
    case 0x54: 
      buttonNumber = 3;
      pinToControl = BUTTON3_PIN;
      break;
    case 0xEA: 
      buttonNumber = 4;
      pinToControl = BUTTON4_PIN;
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
    digitalWrite(pinToControl, HIGH); // Set the pin HIGH for ON state
  } else {
    Serial.println("OFF");
    digitalWrite(pinToControl, LOW);  // Set the pin LOW for OFF state
  }
}
