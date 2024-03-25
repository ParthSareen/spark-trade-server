 #include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define relay1 15
#define relay2 21

const char* ssid = "Parth";
const char* password = "cappingstone";
const char* online = "http://54.202.120.41:8001";
// const char* local = "http://172.20.10.6:8001";
/*
  Example animated analogue meters

  Needs Font 2 (also Font 4 if using large scale label)

  Make sure all the display driver and pin connections are correct by
  editing the User_Setup.h file in the TFT_eSPI library folder.

  #########################################################################
  ###### DON'T FORGET TO UPDATE THE User_Setup.h FILE IN THE LIBRARY ######
  #########################################################################

  Requires widget library here:
  https://github.com/Bodmer/TFT_eWidget
*/

#include <TFT_eSPI.h>     // Hardware-specific library
#include <TFT_eWidget.h>  // Widget library

TFT_eSPI tft  = TFT_eSPI();      // Invoke custom library

MeterWidget   buyer1_display= MeterWidget(&tft);
MeterWidget   buyer2_display= MeterWidget(&tft);
MeterWidget   ohms  = MeterWidget(&tft);

#define LOOP_PERIOD 15 // Display updates every 35 ms

float mapValue(float ip, float ipmin, float ipmax, float tomin, float tomax)
{
  return tomin + (((tomax - tomin) * (ip - ipmin))/ (ipmax - ipmin));
}


String get_wifi_status(int status) {
  switch (status) {
    case WL_IDLE_STATUS:
      return "WL_IDLE_STATUS";
    case WL_SCAN_COMPLETED:
      return "WL_SCAN_COMPLETED";
    case WL_NO_SSID_AVAIL:
      return "WL_NO_SSID_AVAIL";
    case WL_CONNECT_FAILED:
      return "WL_CONNECT_FAILED";
    case WL_CONNECTION_LOST:
      return "WL_CONNECTION_LOST";
    case WL_CONNECTED:
      return "WL_CONNECTED";
    case WL_DISCONNECTED:
      return "WL_DISCONNECTED";
  }
}

String getTrade() {
  String payload = ""; // Initialize payload as an empty string
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    Serial.println("Requesting trade data...");
    String url = String(online) + "/get-trade";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("x-api-key", "secret"); // Use your actual API key
    int httpCode = http.GET();
    if (httpCode > 0) { //Check for the returning code
      payload = http.getString();
      Serial.println(httpCode);
      Serial.println(payload);
    }
    else {
      Serial.println("Error on HTTP GET request");
    }
    http.end(); //Free the resources
  }
  return payload; // Return the payload
}

void clear_trade() {

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    Serial.println("Clearing trade data...");
    String url = String(online) + "/clear-trade";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("x-api-key", "secret"); // Use your actual API key
    int httpCode = http.GET(); // Send the request
    if (httpCode > 0) { // Check for the returning code
      String payload = http.getString(); // Get the request response payload
      Serial.print("HTTP Response code: ");
      Serial.println(httpCode);
      Serial.print("Response payload: ");
      Serial.println(payload);
    }
    else {
      Serial.print("Error on HTTP request, code: ");
      Serial.println(httpCode);
    }
    http.end(); // Free the resources
  }
}
void send_soc_data(float current, float mAh, float voltage) {
if (WiFi.status() == WL_CONNECTED) {

  HTTPClient http;
  Serial.println("Sending SOC data...");
  String url = String(online) + "/send-soc-data";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("x-api-key", "secret"); // Use your actual API key

  // Assuming current, mAh, and voltage are float variables holding the SOC data
  String payload = "{\"current\": " + String(current) + ", \"mAh\": " + String(mAh) + ", \"voltage\": " + String(voltage) + "}";
  
  int httpCode = http.POST(payload);
  if (httpCode > 0) { //Check for the returning code
    String response = http.getString();
    Serial.print("HTTP Response code: ");
    Serial.println(httpCode);
    Serial.print("Response payload: ");
    Serial.println(response);
  }
  else {
    Serial.print("Error on HTTP soc request, code: ");
    Serial.println(httpCode);
  }
  http.end(); //Free the resources
}
else {
  Serial.println("WiFi not connected");
}
}

void create_delay2(int mah_to_trade) {
  for (int i = 0; i < mah_to_trade+1 ; i++) {
    float current = random(19, 21) / 100.0; // Picks a value between 0.25 and 0.26
    float voltage = random(509, 518) / 100.0; // Picks a value between 5.1 and 5.2
    float value_buyer2 = ((float)i/(float)mah_to_trade) * 100.0;
    // float value_buyer2 = i+1;

    // float buyer2_value = mapValue(value_buyer2, (float)0.0, (float)100.0, (float)0.0, (float)100);
    Serial.println("Buyer 2 value");
    Serial.println(value_buyer2);
    buyer2_display.updateNeedle(value_buyer2, 0);
    delay(1000);
    send_soc_data(current, i+1.0, voltage);
  }
}

void create_delay1(int mah_to_trade) {
  for (int i = 0; i < mah_to_trade ; i++) {
    float current = random(25, 27) / 100.0; // Picks a value between 0.25 and 0.26
    float voltage = random(510, 521) / 100.0; // Picks a value between 5.1 and 5.2


    // float value_buyer1 = i+1;
    // float value_buyer1 = ((i)/mah_to_trade) * 100.0;
    float value_buyer1 = ((float)i/(float)mah_to_trade) * 100.0;
    // float buyer1_value = mapValue(value_buyer1, (float)0.0, (float)100.0, (float)0.0, (float)100);
    Serial.println("Buyer 1 value");
    Serial.println(value_buyer1);
    buyer1_display.updateNeedle(value_buyer1, 0);

    delay(1000);
    send_soc_data(current, i+1.0, voltage);
  }
}

void trade_relay1(String mah_to_trade) {
  digitalWrite(relay1, HIGH);
  int mah_to_trade_int = mah_to_trade.toInt();
  create_delay1(mah_to_trade_int);
  digitalWrite(relay1, LOW);
  clear_trade();
}
void trade_relay2(String mah_to_trade) {
  int mah_to_trade_int = mah_to_trade.toInt();
  digitalWrite(relay2, HIGH);
  create_delay2(mah_to_trade_int);
  digitalWrite(relay2, LOW);
  clear_trade();
}


void setup() {
  Serial.begin(115200);
  pinMode(relay1, OUTPUT);
  pinMode(relay2,OUTPUT);
  delay(1000);
  int status = WL_IDLE_STATUS;
  Serial.println("\nConnecting");
  Serial.println(get_wifi_status(status));
  WiFi.begin(ssid, password);
  while (status != WL_CONNECTED) {
    delay(500);
    status = WiFi.status();
    Serial.println(get_wifi_status(status));
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
  int i = 0;

  tft.init();
  tft.setRotation(85);
  Serial.begin(115200); // For debug
  // Colour zones are set as a start and end percentage of full scale (0-100)
  // If start and end of a colour zone are the same then that colour is not used
  //            --Red--  -Org-   -Yell-  -Grn-
  buyer1_display.setZones(0, 25, 25, 50, 50, 75, 75, 100); // Example here red starts at 75% and ends at 100% of full scale
  // Meter is 239 pixels wide and 126 pixels high
  buyer1_display.analogMeter(0, 0, 100.0, "Buyer #1", "0", "25", "50", "75", "100");    // Draw analogue meter at 0, 0

  // Colour draw order is red, orange, yellow, green. So red can be full scale with green drawn
  // last on top to indicate a "safe" zone.
  //             -Red-   -Org-  -Yell-  -Grn-
  buyer2_display.setZones(0, 25, 25, 50, 50, 75, 75, 100);
  buyer2_display.analogMeter(0, 128, 100.0, "Buyer #2", "0", "25", "50", "75", "100");    // Draw analogue meter at 0, 0
 
}

void loop() {
  int  i = 0;
  JsonDocument doc;
  while(true) {
    i++;
    if (i%400000 == 0) {
      i = 0;
      String payload = getTrade();
      deserializeJson(doc, payload);
      String conductTrade = doc["conduct_trade"];
      

      Serial.print("trade status ");
      Serial.println(conductTrade);
      if (conductTrade.equals("True")){
        String mah_to_transmit = doc["mah_to_transmit"];
        String consumer = doc["consumer"];
        Serial.println(consumer);
        if (consumer.equals("Buyer1")) {
          Serial.println("Relay 1 executing trade");
          // digitalWrite(relay1, HIGH);
          // digitalWrite(relay2, HIGH);
          // delay(2000000000);
          // delay(20000);
          // digitalWrite(relay1, LOW);
          // digitalWrite(relay2, LOW);
          trade_relay1(mah_to_transmit);
          // trade_relay2(mah_to_transmit);
        }
        else if (consumer.equals("Buyer2")) {
          Serial.println("Relay 2 executing trade");
          // digitalWrite(relay1, HIGH);
          // digitalWrite(relay2, HIGH);
          // // delay(20000);
          // delay(2000000000);
          // digitalWrite(relay1, LOW);
          // digitalWrite(relay2, LOW);
          trade_relay2(mah_to_transmit);
          // trade_relay1(mah_to_transmit);
        }
      }
      delay(1000);
    }

  }
}
