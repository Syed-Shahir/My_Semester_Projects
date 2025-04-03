#include <LiquidCrystal.h>
#include <Wire.h> // Include the Wire library for I2C communication
#include "RTClib.h" // Include the RTClib for DS137

RTC_DS3231 rtc; // Create an instance of the RTC_DS3231 class

// LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
LiquidCrystal lcd(13, 12, 11, 10, 9, 8);

const int Fan_Pin = 6;
const int Pump_Pin = 7;
const unsigned long motorInterval = 5UL * 1000UL; // Motor runs every 24 seconds
const unsigned long motorDuration = 2UL * 1000UL;  // Motor runs for 2 seconds
unsigned long lastMotorRunTime = 0;
bool motorRunning = false;

void setup() {
  lcd.begin(20, 4); // set up the LCD's number of columns and rows:
  lcd.setCursor(0, 0); // set the cursor position:
  lcd.print(" SMART FARMING    ");

  pinMode(Fan_Pin, OUTPUT);
  pinMode(Pump_Pin, OUTPUT);
  pinMode(A1, INPUT);

  Wire.begin(); // Start the I2C communication
  rtc.begin(); // Initialize the DS137

  // Uncomment the following line if the DS137 lost power and you want to set the time manually.
  // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}

void loop() {
  // Get the current time from DS137
  DateTime now = rtc.now();
  static unsigned long lastUpdateTime = 0;
  unsigned long currentTime = millis();

  // Temperature Sensing 
  int S1 = analogRead(A0);  // Read Temperature
  float mV = (S1 / 1023.0) * 5000; // Storing value in millivolts
  int Temp = mV / 10; // Converting millivolts to degree Celsius
  lcd.setCursor(0, 1);
  lcd.print(" T=");
  lcd.print(Temp);
  lcd.print("'C  ");

  // Soil Moisture
  int S3 = analogRead(A2);  // Read Soil Moisture 
  int SM = S3 / 10;
  lcd.setCursor(0, 2);
  lcd.print(" S=");
  lcd.print(SM);
  lcd.print("%  ");

  // Air Humidity
  int S4 = analogRead(A3);  // Read Air Humidity
  int H = S4 / 10;
  lcd.setCursor(10, 2);
  lcd.print(" H=");
  lcd.print(H);
  lcd.print("%  ");

  // Fan Control
  if (Temp > 30) {
    digitalWrite(Fan_Pin, HIGH);
    lcd.setCursor(0, 3);
    lcd.print(" Fan:ON  ");
  } else {
    digitalWrite(Fan_Pin, LOW);
    lcd.setCursor(0, 3);
    lcd.print(" Fan:OFF ");
  }

  // Motor Control
  if (motorRunning) {
    if (currentTime - lastMotorRunTime >= motorDuration) {
      motorRunning = false;
      digitalWrite(Pump_Pin, LOW);
      lcd.setCursor(10, 3);
      lcd.print(" Motor:OFF ");
    }
  } else {
    if (currentTime - lastMotorRunTime >= motorInterval) {
      if (SM <= 80) { // Only turn on the motor if soil moisture is less than or equal to 80%
        motorRunning = true;
        digitalWrite(Pump_Pin, HIGH);
        lastMotorRunTime = currentTime;
        lcd.setCursor(10, 3);
        lcd.print(" Motor:ON  ");
      } else {
        lcd.setCursor(10, 3);
        lcd.print(" Motor:OFF ");
      }
    }
  }
}
