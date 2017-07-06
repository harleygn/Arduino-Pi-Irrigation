//Include libraries
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2 // Data wire is connected to pin 2

int powerLED = 3; // LED indicating power is connected to pin 3
int statusLED = 4; // LED indicating temperature reading is connected to pin 4
OneWire oneWire(ONE_WIRE_BUS); // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
DallasTemperature sensors(&oneWire); // Pass our oneWire reference to Dallas Temperature. 

void setup(void)
{
  pinMode(statusLED, OUTPUT); // Setup status LED
  pinMode(powerLED, OUTPUT); // Setup power LED
  Serial.begin(9600); //Begin serial communication
  digitalWrite(powerLED, HIGH); // Indicates the board is powered
  Serial.println("Arduino Digital Temperature"); //Print a message
  sensors.begin();
}

void loop(void)
{ 
  digitalWrite(statusLED, HIGH); // Indicates that temperature is being read
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.print("Temperature is: ");
  Serial.println(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  digitalWrite(statusLED, LOW); // Indicates that temperature is no longer being read
  delay(15000); //Update value every 1 sec.
}
