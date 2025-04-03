//replace this with your own

#define BLYNK_TEMPLATE_ID ""
#define BLYNK_TEMPLATE_NAME ""

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
//replace this with your own
#define BLYNK_AUTH_TOKEN ""
#define IN1 D1
#define IN2 D2
#define IN3 D3
#define IN4 D4

char auth[] = BLYNK_AUTH_TOKEN;
char ssid[] = "";  // Enter your WIFI name
char pass[] = "";  // Enter your WIFI password

void setup() {

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
//Blynk.begin() establishes the connection between your hardware and the Blynk server, 
//enabling communication for remote control and data exchange with the Blynk app or cloud platform.
  Blynk.begin(auth, ssid, pass, "blynk.cloud", 80);
}

void loop() {
  Blynk.run();
}
//BLYNK_WRITE(virtual_pin) is a special function called a "Virtual Pin" handler. 
//These functions are automatically invoked by the Blynk library when the corresponding
// virtual pin in the Blynk app changes its state or value.
BLYNK_WRITE(V0) {
  //When a BLYNK_WRITE(Vx) function is called (where Vx is a virtual pin number), 
  //param represents the value or state sent from the corresponding widget in the Blynk app that triggered the function call.
  int buttonState = param.asInt();
  if (buttonState == 1) {
    carForward();
  } else {
    carStop();
  }
}

BLYNK_WRITE(V1) {
  int buttonState = param.asInt();
  if (buttonState == 1) {
    carBackward();
  } else {
    carStop();
  }
}

BLYNK_WRITE(V2) {
  int buttonState = param.asInt();
  if (buttonState == 1) {
    carLeft();
  } else {
    carStop();
  }
}

BLYNK_WRITE(V3) {
  int buttonState = param.asInt();
  if (buttonState == 1) {
    carRight();
  } else {
    carStop();
  }
}

void carForward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void carBackward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void carLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void carRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void carStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
