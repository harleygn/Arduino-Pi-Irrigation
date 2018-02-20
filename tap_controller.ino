// Indicates which pin the solenoid is connected to
int solenoidPin = 4;
// Declares an empty string to hold incoming data
String inputString = "";
// Indicates whether the incoming string is complete
boolean stringComplete = false;
// Indicates the connection status to the hub
boolean connection = false;

void setup() {
  // Begins serial transmission with Baud rate 9600
  Serial.begin(9600);
  // Sets the pins as outputs
  pinMode(solenoidPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
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
    if (stringComplete and connection == true) {
      // If the command to open the tap is received
      if (inputString == "on")
        // Opens the valve
        tapControl(true);
      // If the command to close the tap is received
      else if (inputString == "off")
        // Closes the valve
        tapControl(false);
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

// Opens/closes the valve and sets the LED depending on the command
void tapControl(boolean command) {
  if (command == true) {
    // Switches Solenoid ON
    digitalWrite(solenoidPin, HIGH);
    // Switches indicator LED ON
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (command == false) {
    //Switches Solenoid OFF
    digitalWrite(solenoidPin, LOW);
    // Switches indicator LED OFF
    digitalWrite(LED_BUILTIN, LOW);
  }
  // Closes the connecton status
  connection = false;
}
