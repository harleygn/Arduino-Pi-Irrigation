// Include libraries for communicating with the sensor and RTC, and handling time
#include "DHT.h"
#include <DS1307RTC.h>
#include <Time.h>
#include <Timezone.h>

// Timezone configuration
// BST begins on the last Sunday of March
TimeChangeRule myBST = {"BST", Last, Sun, Mar, 1, +60};
// UTC returns on the last Sunday in October
TimeChangeRule myGMT = {"UTC", Last, Sun, Oct, 1, -60};
// Creates timezone object with the rules set above
Timezone myTZ(myBST, myGMT);

// Pointer to the time change rule to get TZ abbrev
TimeChangeRule *tcr;
// Sets the local time to GMT
time_t gmt, local;

// Specifies which digital pin the sensor is connected to
#define DHTPIN 2 
// Specifies which type og DHT sensor is in use
#define DHTTYPE DHT11

// Declares an empty string to hold incoming data
String inputString = "";
// Indicates whether the incoming string is complete
boolean stringComplete = false;
// Indicates the connection status to the hub
boolean connection = false;

// Initializes the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Begins serial transmission with Baud rate 9600
  Serial.begin(9600);
  // Initiates the sensor
  dht.begin();
  // Gets the time from the RTC
  setSyncProvider(RTC.get);
  // Returns an error if unable to set the time using the RTC
  if(timeStatus()!= timeSet)
    Serial.println("Unable to sync with the RTC");
  // Reserves 200 bytes for the inputString
  inputString.reserve(200);
}

void loop() {
  // Syncs the current time with the local time
  gmt = now();
  // Syncs the current time with the local time according to the timezone
  local = myTZ.toLocal(gmt, &tcr);
  // What to do when the string is complete
  if (stringComplete) {
    // Trims off the new line ending characters
    inputString.trim();
    // If the controller receives a call
    if (inputString == "call") {
      // Returns a response to initiate connection
      Serial.println("response");
      // Sets the connection status
      connection = true;
    }
    if (stringComplete and connection) {
      // If the received command matches the data request command
      if (inputString == "datarequest") {
        // Pointer for accessing members of class instance
        // Builds the data package from the timestamp and sensor readings
        String dataPackage = (buildTime(local, tcr -> abbrev)) + getReadings();
        // Sends the data package over serial
        Serial.println(dataPackage);
        // Resets the Boolean flag
        connection = false;
      }
    }

    // Clears the input string for new data
    inputString = "";
    // Resets the Boolean flag
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware
  serial RX and is run between each run of the loop()
*/
void serialEvent() {
  // If there is data in the serial buffer
  while (Serial.available()) {
    // Get the new byte
    char inChar = (char)Serial.read();
    // Add it to the inputString to build up the message
    inputString += inChar;
    // The new line charcter indicates the message is complete
    if (inChar == '\n') {
      // Set the global flag to indciate the message is complete
      stringComplete = true;
    }
  }
}

// Gets temperature and humidity readings from the sensor
String getReadings() {
  // Read temperature as Celsius and multiplies it to get an integer
  int t = (dht.readTemperature() * 100);
  // Read humidity as percentage, which is already and integer
  int h = dht.readHumidity();
  // Check if any reads failed and exit early (to try again)
  if (isnan(h) || isnan(t)) {
    // Sends the error
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  // Combines the two readings into a single integer
  return (String(t) + String(h));
}

// Builds a timestamp with time zone adjustment
String buildTime(time_t t, char *tz) {
  // Gets the two-digit hour value
  String hr = addLeadingZeros(hour(t));
  // Gets the two-digit minute value
  String min = addLeadingZeros(minute(t));
  // Build a four-digit timestamp
  return (hr + min);
}

// Returns an integer in "00" format (with leading zero)
// Input value assumed to be between 0 and 99
String addLeadingZeros(int val) {
  String time;
  // Checks if a leading 0 is necessary
  if (val < 10)
  // Adds a leading 0
    time += ("0"); // Adds a leading 0
  // Completes the value
  time += (val);
  // Returns the value as string
  return time;
}
