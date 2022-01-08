#include "arm.h"
#include "wifi.h"
#include "request.h"
#include "server.h"
void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);  
/*  for(int ang=0; ang<180; ang++){
    s[0].write(ang);
    delay(15);
  }
  for(int ang=180; ang>0; ang--){
    s[0].write(ang);
    delay(15);
  }*/

  WiFiConnect();
  init_wifi();
  webserver_setup();
}

void loop() {
  MDNS.update();
  handle_client();
//    request();
//  delay(1000);
}
