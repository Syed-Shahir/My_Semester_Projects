// HardwareSerial dwin(2); // Use UART2 for communication with DWIN (TX2, RX2)

// void setup() {
//   Serial.begin(115200);                // For debugging via Serial Monitor
//   dwin.begin(115200, SERIAL_8N1, 16, 17); // Initialize UART2 (RX2 = GPIO 16, TX2 = GPIO 17)
// }

// // void loop() {
// //   while (dwin.available()) {
// //     uint8_t data = dwin.read();
// //     Serial.print("0x");
// //     Serial.print(data, HEX); // Print as hexadecimal
// //     Serial.print(" ");
// //   }
// // }

// void loop() {
//   static uint8_t buffer[64];
//   static size_t index = 0;

//   while (dwin.available()) {
//     uint8_t data = dwin.read();
//     buffer[index++] = data;

//     // Example: If you know each frame is 8 bytes
//     if (index == 8) {
//       Serial.print("Frame: ");
//       for (size_t i = 0; i < index; i++) {
//         Serial.print("0x");
//         Serial.print(buffer[i], HEX);
//         Serial.print(" ");
//       }
//       Serial.println();
//       index = 0; // Reset for next frame
//     }
//   }
//   //delay(50);
// }



// HardwareSerial dwin(2); // Use UART2 for communication with DWIN (TX2, RX2)

// unsigned char Buffer[8];  // Buffer to store the received frame

// void setup() {
//   Serial.begin(115200);                // For debugging via Serial Monitor
//   dwin.begin(115200, SERIAL_8N1, 16, 17); // Initialize UART2 (RX2 = GPIO 16, TX2 = GPIO 17)
//   Serial.println("Ready to receive and display frames...");
// }

// void loop() {
//   // Check if there's enough data for at least one frame (8 bytes)
//   if (dwin.available() >= 8) {
//     // Shift data until we find the start byte (0xA9)
//     while (dwin.available() > 0) {
//       unsigned char byte = dwin.read();
//       if (byte == 0xA9) { // Start byte found
//         Buffer[0] = byte;

//         // Read the remaining 7 bytes of the frame
//         for (int i = 1; i < 8; i++) {
//           while (!dwin.available()); // Wait for each byte
//           Buffer[i] = dwin.read();
//         }

//         // Display the aligned frame (print in hexadecimal)
//         Serial.print("Aligned Frame: ");
//         for (int i = 0; i < 8; i++) {
//           Serial.print("0x");
//           if (Buffer[i] < 0x10) Serial.print("0"); // Add leading zero for single-digit hex
//           Serial.print(Buffer[i], HEX);
//           Serial.print(" ");
//         }
//         Serial.println();
//         break; // Exit the while loop after processing a frame
//       }
//     }
//   }
// }

#include <HardwareSerial.h>

HardwareSerial dwin(2); // Use UART2 for communication with DWIN (TX2, RX2)

unsigned char Buffer[8];  // Buffer to store the received frame

void setup() {
  Serial.begin(115200);                // For debugging via Serial Monitor
  dwin.begin(115200, SERIAL_8N1, 16, 17); // Initialize UART2 (RX2 = GPIO 16, TX2 = GPIO 17)
  Serial.println("Ready to receive and display frames...");
}

void loop() {
  // Check if there's enough data for at least one frame (8 bytes)
  if (dwin.available() >= 8) {
    // Shift data until we find the start byte (0xA9)
    while (dwin.available() > 0) {
      unsigned char byte = dwin.read();
      if (byte == 0xA9) { // Start byte found
        Buffer[0] = byte;

        // Read the remaining 7 bytes of the frame
        for (int i = 1; i < 8; i++) {
          while (!dwin.available()); // Wait for each byte
          Buffer[i] = dwin.read();
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

        // Identify the button and status
        identifyButtonAndStatus(Buffer[3], Buffer[6]);
        break; // Exit the while loop after processing a frame
      }
    }
  }
  delay(50); // Add small delay to stabilize state reading and prevent over-processing
}

// Function to identify button and ON/OFF status
void identifyButtonAndStatus(unsigned char buttonByte, unsigned char stateByte) {
  int buttonNumber;

  // Map the 4th byte to the corresponding button number
  switch (buttonByte) {
    case 0x55: buttonNumber = 1; break;
    case 0xAA: buttonNumber = 2; break;
    case 0x54: buttonNumber = 3; break;
    case 0xEA: buttonNumber = 4; break;
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



