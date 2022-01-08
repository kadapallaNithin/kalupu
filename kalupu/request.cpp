#include "request.h"
WiFiClient client;
HTTPClient http;
String server_address = "";
void request(String address){
  if(WiFi.status() != WL_CONNECTED) {
    WiFiConnect();
  }
  STDLOG.print("[HTTP] begin...\n");
  if (http.begin(client, address )) {  // HTTP
    STDLOG.print("[HTTP] GET...\n");
      // start connection and send HTTP header
    int httpCode = http.GET();
      // httpCode will be negative on error
    if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
      STDLOG.printf("[HTTP] GET... code: %d\n", httpCode);
        // file found at server
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
        String payload = http.getString();
        STDLOG.println(payload);
      }
    } else {
      STDERR.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  } else {
    STDERR.printf("[HTTP} Unable to connect\n");
  }
}
