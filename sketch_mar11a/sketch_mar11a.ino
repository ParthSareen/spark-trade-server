#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
void setup() {
  // put your setup code here, to run once:
  char ssid[] = "Datacity 661";
  char pass[] = "12345678";
//  char* addr = "192.168.0.100 ";
//  uint16_t port  = 10101;
  Serial.begin(115200);
  WiFiClient  client;
  Serial.print("Setting up WIFI for SSID ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) {
   Serial.println("WIFI connection failed, reconnecting...");
   delay(500);
  }
  
  Serial.println("");
  Serial.print("WiFi connected, ");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Your URL for the GET request
    http.begin("http://54.202.120.41:8001/get-command-arduino");
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.GET();
    
    if (httpCode > 0) { //Check for the returning code
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);
      }
    else {
      Serial.println("Error on HTTP request");
    }
    http.end(); //Free the resources
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
