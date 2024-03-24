#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define relay1 15
#define relay2 23

const char* ssid = "Parth";
const char* password = "cappingstone";
const char* online = "http://54.202.120.41:8001"
const char* local = "http://172.20.10.6:8001"

String getWifiStatus(int status) {
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
      Serial.println("Error on HTTP request");
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
    http.addHeader("x-api-key", "secret"); // Use your
}
void send_soc_data() {}
void trade_relay1() {
  digitalWrite(relay1, HIGH);
  // TODO: figure delay portion out
  delay(3000);
  digitalWrite(relay1, LOW);
  clear_trade();
}
void trade_relay2() {}


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
    if (i%40000 == 0) {
      i = 0;
      String payload = getTrade();
      deserializeJson(doc, payload);
      String conductTrade = doc["conductTrade"];

      if (conductTrade == "True") {
        String consumer = doc["consumer"];
        if (consumer == "Buyer1") {
          trade_relay1();
        }
        else if (consumer == "Buyer2") {
          trade_relay2();
        }
      }
    }

  }
  // while(true){
  //   i++;
  //   if (i%10000 == 0) {
  //     i = 0;
  //     if (WiFi.status() == WL_CONNECTED) {
  //       HTTPClient http;
  //       Serial.println("sending req");
  //     // Your URL for the GET request 172.20.10.6
  // //    http.begin("http://54.202.120.41:8001/get-command-arduino");
  //       http.begin("http://172.20.10.6:8001/test/1");
  //       http.addHeader("Content-Type", "application/json");
  //       http.addHeader("x-api-key", "secret");
  //       int httpCode = http.GET();
  //       String payload = http.getString();
        
  //       Serial.println(httpCode);
  //       Serial.println(payload);
  //       deserializeJson(doc, payload);
  
  //       int relay_value = doc["number"];
  
  //       Serial.println(relay_value);
  //       if (relay_value == 1);
  //         digitalWrite(relay1, HIGH);
  //         delay(3000);
  //         digitalWrite(relay1, LOW);
  //       }
  //     else {
  //       Serial.println("WIFI fucked up");
  //       }
  //     }
  //   }

// while(true) {
//   if (WiFi.status() == WL_CONNECTED) {
//     HTTPClient http;
//     Serial.println("sending POST req");
//     http.begin("http://172.20.10.6:8001/test_post"); // Your URL for the POST request
//     http.addHeader("Content-Type", "application/json");
//     http.addHeader("x-api-key", "secret");

//     // Create JSON object to send
//     StaticJsonDocument<200> jsonDoc;
//     jsonDoc["device"] = "ESP32";
//     jsonDoc["status"] = "active";
//     String requestBody;
//     serializeJson(jsonDoc, requestBody);

//     int httpCode = http.POST(requestBody);
//     String payload = http.getString();

//     Serial.println(httpCode);
//     Serial.println(payload);
//   }
//   else {
//     Serial.println("WIFI not connected");
//   }
//   delay(10000); // Wait for 10 seconds before the next iteration
// }

}
