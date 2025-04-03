#include <ESP8266WiFi.h>
//scanning and connecting to wifi network
const char* ssid = "";//wifi name
const char* password = "";//wifi password

void setup() {
    pinMode(D4, OUTPUT); // Set the built-in LED pin as outpu
   Serial.begin(9600);
  delay(1000);
  WiFi.mode(WIFI_STA);
  Serial.println("Scanning for Wi-Fi networks...");

  // Start scanning for Wi-Fi networks
  int numNetworks = WiFi.scanNetworks();

  if (numNetworks == 0) {
    Serial.println("No Wi-Fi networks found.");
  } else {
    Serial.print("Found ");
    Serial.print(numNetworks);
    Serial.println(" Wi-Fi networks:");

    for (int i = 0; i < numNetworks; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(" dBm)");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      delay(10);
    }
  }
 

  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");

  while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(D4, HIGH); // Turn on the LED
  delay(100); // Wait for 1 second
  digitalWrite(D4, LOW); // Turn off the LED
  delay(100); // Wait for 1 second
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected to Wi-Fi network. IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
    digitalWrite(D4, HIGH); // Turn on the LED
  delay(50); // Wait for 1 second
  digitalWrite(D4, LOW); // Turn off the LED
  delay(50); // Wait for 1 second
  // Your code here
}


