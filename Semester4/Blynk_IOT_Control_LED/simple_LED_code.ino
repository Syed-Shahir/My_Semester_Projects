//these must be placed at the beggining of the program otherwise you may face an error
#define BLYNK_TEMPLATE_ID ""
#define BLYNK_TEMPLATE_NAME ""

#include<ESP8266WiFi.h>
#include<BlynkSimpleEsp8266.h>

#define BLYNK_AUTH_TOKEN ""



char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "";         //Wifi name
char pass[] = "";   //Password


void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // Set built-in LED pin as output
  //This function initiates a connection to the Blynk cloud server using the Blynk authentication token,
  // Wi-Fi network details, Blynk server address, and port number.
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
}

BLYNK_WRITE(V0) {
  //Retrieves the value sent from the Blynk app.
  int value = param.asInt(); // Get value from Blynk app
  if (value == 1) {
    digitalWrite(LED_BUILTIN, HIGH); // Turn on LED
  } else {
    digitalWrite(LED_BUILTIN, LOW); // Turn off LED
  }
}

void loop() {
  // It constantly checks for incoming commands or instructions from the Blynk app.
  Blynk.run();
}
