#include "wifi.h"
String ssid  = "kadapalla";
//used_by : wifi/request()
String password = "12345678";
WiFiEventHandler gotIpEventHandler, disconnectedEventHandler;
void init_wifi(){
//  pinMode(ONLINE_LED_PIN,OUTPUT);
  WiFi.mode(WIFI_STA);
  /*gotIpEventHandler = WiFi.onStationModeGotIP([](const WiFiEventStationModeGotIP& event)
  {
    digitalWrite(ONLINE_LED_PIN,HIGH);
  });

  disconnectedEventHandler = WiFi.onStationModeDisconnected([](const WiFiEventStationModeDisconnected& event)
  {
    digitalWrite(ONLINE_LED_PIN,LOW);
  });*/
  STDLOG.println("Attempt to begin MDNS");
  if (!MDNS.begin("kadapalla")) {
    STDERR.println("Error setting up MDNS responder!");
    while (1) {
      delay(1000);
    }
  }
  STDLOG.println("MDNS Begun");
//  server.begin();
  MDNS.addService("http", "tcp", 80);
}
String IpAddress2String(const IPAddress& ipAddress)
{
  return String(ipAddress[0]) + String(".") +\
  String(ipAddress[1]) + String(".") +\
  String(ipAddress[2]) + String(".") +\
  String(ipAddress[3]);
}
String WiFiConnect(){
  STDLOG.print("Connecting to ");
  STDLOG.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    STDOUT.print(".");
  }
  String ip = IpAddress2String(WiFi.localIP());
  STDLOG.print("IP address: ");
  STDLOG.println(ip);
  return ip;
}
void ensure_connect(){
  if (WiFi.status() != WL_CONNECTED) {
    WiFiConnect();
  }  
}
