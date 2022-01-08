#ifndef nithin_wifi_h
#define nithin_wifi_h
#include <ESP8266WiFi.h>
#include <ESP8266mDNS.h>
#include <WiFiClient.h>
#define STDOUT Serial1
#define STDLOG Serial1
#define STDERR Serial1
extern String updateUrl;
//void handle_client();
void init_wifi();
String WiFiConnect();
void ensure_connect();
#endif
