#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Wi-Fi credentials for Access Point
const char* ssid = "ESP8266_AP";
const char* password = "12345678";

// Create a web server on port 80
ESP8266WebServer server(80);

// Appliance pins
#define LIGHT_PIN D0  // Controlled by Button 1
#define FAN_PIN D1    // Controlled by Button 2
#define AC_PIN D2     // Controlled by Button 3
#define TV_PIN D3     // Controlled by Button 4

unsigned char Buffer[8];  // For DWIN display frames

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing...");

  // Configure appliance pins as output
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);
  pinMode(AC_PIN, OUTPUT);
  pinMode(TV_PIN, OUTPUT);

  // Turn all appliances OFF initially
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(AC_PIN, LOW);
  digitalWrite(TV_PIN, LOW);

  // Set up ESP8266 as Access Point
  WiFi.softAP(ssid, password);
  Serial.println("Access Point Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());

  // Define server routes for Wi-Fi control
  server.on("/light/on", []() {
    digitalWrite(LIGHT_PIN, HIGH);
    server.send(200, "text/plain", "Light ON");
  });

  server.on("/light/off", []() {
    digitalWrite(LIGHT_PIN, LOW);
    server.send(200, "text/plain", "Light OFF");
  });

  server.on("/fan/on", []() {
    digitalWrite(FAN_PIN, HIGH);
    server.send(200, "text/plain", "Fan ON");
  });

  server.on("/fan/off", []() {
    digitalWrite(FAN_PIN, LOW);
    server.send(200, "text/plain", "Fan OFF");
  });

  server.on("/ac/on", []() {
    digitalWrite(AC_PIN, HIGH);
    server.send(200, "text/plain", "AC ON");
  });

  server.on("/ac/off", []() {
    digitalWrite(AC_PIN, LOW);
    server.send(200, "text/plain", "AC OFF");
  });

  server.on("/tv/on", []() {
    digitalWrite(TV_PIN, HIGH);
    server.send(200, "text/plain", "TV ON");
  });

  server.on("/tv/off", []() {
    digitalWrite(TV_PIN, LOW);
    server.send(200, "text/plain", "TV OFF");
  });

  // Start the server
  server.begin();
  Serial.println("Web Server Started");
}

void loop() {
  // Handle Wi-Fi client requests
  server.handleClient();

  // Handle DWIN display commands
  handleDWINInput();
}

// Function to handle DWIN display input
void handleDWINInput() {
  if (Serial.available() >= 8) {
    // Read the DWIN frame
    while (Serial.available() > 0) {
      unsigned char byte = Serial.read();
      if (byte == 0xA9) { // Start byte found
        Buffer[0] = byte;

        for (int i = 1; i < 8; i++) {
          while (!Serial.available()); // Wait for each byte
          Buffer[i] = Serial.read();
        }

        // Identify and process button and state
        identifyButtonAndControlPins(Buffer[3], Buffer[6]);
        break;
      }
    }
  }
}

// Function to identify button and control GPIO pins
void identifyButtonAndControlPins(unsigned char buttonByte, unsigned char stateByte) {
  int pinToControl;

  // Map the button to the corresponding pin
  switch (buttonByte) {
    case 0x55: pinToControl = LIGHT_PIN; break; // Button 1
    case 0xAA: pinToControl = FAN_PIN; break;   // Button 2
    case 0x54: pinToControl = AC_PIN; break;    // Button 3
    case 0xEA: pinToControl = TV_PIN; break;    // Button 4
    default: 
      Serial.println("Unknown Button");
      return;
  }

  // Determine ON/OFF state
  bool isOn = (stateByte == 0xFD); // ON if 0xFD, OFF if 0xFF

  // Control the pin
  digitalWrite(pinToControl, isOn ? HIGH : LOW);

  // Print the status
  Serial.print("Button ");
  Serial.print(buttonByte, HEX);
  Serial.print(" -> ");
  Serial.println(isOn ? "ON" : "OFF");
}

