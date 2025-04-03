#include <ESP8266WiFi.h>
//scanning and printing wifi networks
void setup() {
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
}

void loop() {
  // Your code here
}
