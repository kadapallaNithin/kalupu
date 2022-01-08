#ifndef nithin_server_h
#define nithin_server_h
#include <ESP8266WebServer.h>
#include "wifi.h" // STDLOG
#include "request.h"
#include "httpUpdate.h"
#include "servo.h"
#define VERSION 9
void webserver_setup();
void handle_client();
#endif
