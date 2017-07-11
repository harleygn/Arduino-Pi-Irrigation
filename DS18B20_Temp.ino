// Include libraries
#include <OneWire.h>            // For comunicating using OneWire
#include <Wire.h>               // For communcating using i2c
#include <DallasTemperature.h>  // For communicating with the DS18B20 sensor
#include <DS1307RTC.h>          // For communicating with the DS1307 RTC
#include <Time.h>               // A dependancy for the Timezone library
#include <Timezone.h>           // Allows the time to be displayed according to the timezone and BST

#define ONE_WIRE_BUS 2 // DS18B20 data wire is connected to pin 2

int powerLED = 3; // LED indicating power is connected to pin 3
int statusLED = 4; // LED indicating temperature reading is connected to pin 4
OneWire oneWire(ONE_WIRE_BUS); // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
DallasTemperature sensors(&oneWire); // Pass our oneWire reference to Dallas Temperature. 

// Timezone configuration
TimeChangeRule myBST = {"BST", Last, Sun, Mar, 1, +60}; //BST = GMT + 1 hour
TimeChangeRule myGMT = {"GMT", Last, Sun, Oct, 1, -60}; //GMT = UTC
Timezone myTZ(myBST, myGMT); // Creates timezone object with the rules set above

TimeChangeRule *tcr; // Pointer to the time change rule to get TZ abbrev
time_t gmt, local; // Sets the local time to GMT

void setup(void)
{
  pinMode(statusLED, OUTPUT); // Setup status LED
  pinMode(powerLED, OUTPUT); // Setup power LED
  digitalWrite(powerLED, HIGH); // Indicates the board is powered
  Serial.begin(9600); // Initiate serial output at Buad rate 9600
  setSyncProvider(RTC.get); // Function to get the time from the RTC
  if(timeStatus()!= timeSet) // Returns and error if unable to set the time using the RTC
    Serial.println("Unable to sync with the RTC"); // Returned error
}

void loop(void)
{
  Serial.println();
  gmt = now(); // Syncs the current time with the local time
  local = myTZ.toLocal(gmt, &tcr); // Syncs the current time with the local time according to the timezone
  printTime(local, tcr -> abbrev); // Poiner for accessing members of class instance
  Serial.print(" ");
  digitalWrite(statusLED, HIGH); // Indicates that temperature is being read
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  digitalWrite(statusLED, LOW); // Indicates that temperature is no longer being read
  Serial.println();
  delay(15000); // Update value every 15 seconds
}

// Function to print time with time zone adjustment
void printTime(time_t t, char *tz)
{
  sPrintI00(day(t));
  Serial.print('/');
  Serial.print(month(t));
  Serial.print('/');
  Serial.print(year(t));
  Serial.print(' ');
  sPrintI00(hour(t));
  sPrintDigits(minute(t));
  sPrintDigits(second(t));
}

// Print an integer in "00" format (with leading zero)
// Input value assumed to be between 0 and 99
void sPrintI00(int val)
{
  if (val < 10)
    Serial.print('0'); // Checks if a leading 0 is necessary
  Serial.print(val, DEC);
  return;
}

// Print an integer in ":00" format (with leading zero)
// Input value assumed to be between 0 and 99
void sPrintDigits(int val)
{
  Serial.print(':');
  if(val < 10)
    Serial.print('0'); // Checks if a leading 0 is necessary
  Serial.print(val, DEC);
}
