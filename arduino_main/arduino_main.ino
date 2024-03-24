 #include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define relay1 15
#define relay2 23

const char* ssid = "Parth";
const char* password = "cappingstone";
const char* online = "http://54.202.120.41:8001";
const char* local = "http://172.20.10.6:8001";

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
    String url = String(local) + "/get-trade";
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
    String url = String(local) + "/clear-trade";
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
  String url = String(local) + "/send-soc-data";
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
  for (int i = 0; i < mah_to_trade ; i++) {
    float current = random(19, 21) / 100.0; // Picks a value between 0.25 and 0.26
    float voltage = random(509, 518) / 100.0; // Picks a value between 5.1 and 5.2
    delay(1000);
    send_soc_data(current, i+1.0, voltage);
  }
}

void create_delay1(int mah_to_trade) {
  for (int i = 0; i < mah_to_trade ; i++) {
    float current = random(25, 27) / 100.0; // Picks a value between 0.25 and 0.26
    float voltage = random(510, 521) / 100.0; // Picks a value between 5.1 and 5.2
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
          trade_relay1(mah_to_transmit);
        }
        else if (consumer.equals("Buyer2")) {
          Serial.println("Relay 2 executing trade");
          trade_relay2(mah_to_transmit);
        }
      }
      delay(1000);
    }

  }
}
