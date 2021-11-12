#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

/* this can be run with an emulated server on host:
        cd esp8266-core-root-dir
        cd tests/host
        make ../../libraries/ESP8266WebServer/examples/PostServer/PostServer
        bin/PostServer/PostServer
   then put your PC's IP address in SERVER_IP below, port 9080 (instead of default 80):
*/

/* !!! THESE values you need to change on yours (local server address, essid and bssid(password) for) */
#define SERVER_IP "http://192.168.2.100:5000/"

#ifndef STASSID
#define STASSID "ЖАК ДАСЬКО"
#define STAPSK  "1945hrb1327a"
#endif
/* also, you can try change delay between POST requests (in case of inaccurate work set bigger value) */

unsigned long lastTime = 0;
unsigned long timerDelay = 8000;

#define USE_ARDUINO_INTERRUPTS false // не работает с прерываниями, nodemcu вылетает в бесконечный -2 segfault
#include <PulseSensorPlayground.h>

const int PULSE_INPUT = A0;
const int PULSE_BLINK = 2;    // Pin 13 is the on-board LED
const int PULSE_FADE = 5;
const int THRESHOLD = 550;   // Adjust this number to avoid noise when idle
PulseSensorPlayground pulseSensor;
const int OUTPUT_TYPE = SERIAL_PLOTTER; // in debugging purposes

byte samplesUntilReport;
const byte SAMPLES_PER_SERIAL_SAMPLE = 10;

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println();

  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  pulseSensor.analogInput(PULSE_INPUT);
  pulseSensor.blinkOnPulse(PULSE_BLINK);
  pulseSensor.fadeOnPulse(PULSE_FADE);

  pulseSensor.setSerial(Serial);
  pulseSensor.setOutputType(OUTPUT_TYPE);
  pulseSensor.setThreshold(THRESHOLD);

  // Skip the first SAMPLES_PER_SERIAL_SAMPLE in the loop().
  samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;

  if (!pulseSensor.begin()) {
    for(;;) {
      // Flash the led to show things didn't work.
      digitalWrite(PULSE_BLINK, LOW);
      delay(50);
      digitalWrite(PULSE_BLINK, HIGH);
      delay(50);
    }
  }
}

void loop() {
  int myBPM = pulseSensor.getBeatsPerMinute();
  Serial.println(myBPM);
  Serial.println(millis() - lastTime);
  
  if (pulseSensor.sawNewSample()) {
    if (--samplesUntilReport == (byte) 0) {
      samplesUntilReport = SAMPLES_PER_SERIAL_SAMPLE;

      pulseSensor.outputSample();
      if (pulseSensor.sawStartOfBeat()) {
        pulseSensor.outputBeat();
      }
    }

    if ((WiFi.status() == WL_CONNECTED) && ((millis() - lastTime) > timerDelay)) {

      WiFiClient client;
      HTTPClient http;

      Serial.print("[HTTP] begin...\n");
      // configure traged server and url
      http.begin(client, SERVER_IP); //HTTP
      http.addHeader("Content-Type", "application/json");

      Serial.print("[HTTP] POST...\n");
      // start connection and send HTTP header and body
      String s1 = String("{\"pulse\":") + String(myBPM) + String("}");
      int httpCode = http.POST(s1);

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] POST... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK) {
          const String& payload = http.getString();
          Serial.println("received payload:\n<<");
          Serial.println(payload);
          Serial.println(">>");
        }
      } 
      else {
        Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
      lastTime = millis();
    }
  }
}
