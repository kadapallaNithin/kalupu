#include "server.h"
ESP8266WebServer webserver(80);
int system_mode = 1; //2axis & 1servo, 3 axis & 3 servo...
String updateUrl = "http://10.42.0.1:8000/product/0/update/";
String file_data = String();
char waitNread(){
  while(!Serial.available()){
    ;
  }
  return Serial.read();
}
String waitNreadStringUntil(char c){
  while(!Serial.available()){
    ;
  }
  return Serial.readStringUntil(c);
}
void handleServoSystemSetting(){
  String response = "";
  if(webserver.args() == 2){
    servo_system.set_settings(webserver.arg(0));
  }
  response += servo_system.get_settings();
  webserver.send(200, "text/plain",response);
}
void handleBlink(){
  int time_period = 1000;
  int number_of_times = 10;
  if(webserver.args()>1){
    if(webserver.argName(0) == "time period"){
      time_period = webserver.arg(0).toFloat()*1000;
    }
    if(webserver.args() > 2 && webserver.argName(1) == "number of times"){
      number_of_times = webserver.arg(1).toInt();
    }
  }
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", "Blinking with time period "+String(time_period/1000.0)+"sec. For "+String(number_of_times)+" times");
  for(int i=0; i<number_of_times; i++){
    digitalWrite(LED_BUILTIN,LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN,HIGH);
    delay(1000);
    Serial.print(i);
    Serial.println("blink");
  }
}
void handleUpdate(){
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", "Updating from url : "+updateUrl+"\nVersion before update"+String(VERSION));
  httpUpdate();
}
void handleVersion(){
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", String(VERSION));
}
bool is_start_of_gcode(char c){
  return (c == 'G' || c == 'g');//|| c == 'M' || c == 'm');
}
/*void updateServoPins(){
  String response;
  if(webserver.args() > 1 && webserver.argName(0) == "pins"){
    servo_data_not_used.set_servo_pin(0,webserver.arg(0).substring(webserver.arg(0).indexOf('a')+1).toInt());
    servo_data_not_used.set_servo_pin(1,webserver.arg(0).substring(webserver.arg(0).indexOf('b')+1).toInt());
    servo_data_not_used.set_servo_pin(2,webserver.arg(0).substring(webserver.arg(0).indexOf('c')+1).toInt());
    response = "Updated servo pins are: a"+String(servo_data_not_used.get_servo_pin(0))+" b"+String(servo_data_not_used.get_servo_pin(1))+" c"+String(servo_data_not_used.get_servo_pin(2));
  }
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", response);
  servo_data_not_used.init_servos();  
}*/
void setSystemMode(){
  String response;
  if(webserver.args() == 2 && webserver.argName(0) == "mode"){
    system_mode = webserver.arg(0).toInt();
  }
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", response);
}
void setUpdateUrl(){
  String response = "Please give only one data item with name url";
  if(webserver.args() == 2 && webserver.argName(0) == "url"){
    response = "Url was "+updateUrl;
    updateUrl = webserver.arg(0);
    response += "\nUrl updated to "+updateUrl;
  }
  webserver.sendHeader("Access-Control-Allow-Origin","*");
  webserver.send(200, "text/plain", response);
}
void handleGCodeLine(String line){
  line.toUpperCase();
  if(is_start_of_gcode(line[0])){
    if(system_mode == 1){
      int z_pos = line.indexOf('Z');
      if(z_pos != -1){
        float z = line.substring(z_pos+1,z_pos+9).toFloat();
        if(z > 20){
          servo_system.sweep(0);
        }else if(z == -2){
          servo_system.down(0);
        }else if(z == 3){
          servo_system.up(0);
        }
      }else{
      Serial.println(line);
      waitNreadStringUntil('\n');
      }
    }
  }
}
/*void handleGCodeFast(){
  if(webserver.method() == HTTP_POST){
    if(webserver.args() == 2 && webserver.argName(0) == "gcode"){
//     Serial.println(webserver.arg(0));
      char block[64];
      int sending_state = 0;// don't send = 0, should take z action = 1, send = 2, send and take z action = 3
      int bl_len = 0, l_len = 0, z_ind = -1, l_begining = 0, len = webserver.arg(0).length();
      for(int i=0; i<len; i++){
        char ci = webserver.arg(0)[i];
        block[bl_len+l_len++] = ci;
        
          if(z_ind != -1){
             block[bl_len+l_len] = '\0';// check off by one
             Serial.println(block);
          }
        if(bl_len + l_len >= 63){
          block[bl_len] = '\0';
          Serial.println(block);
          for(int cp_itr=0; cp_itr < l_len; cp_itr++){
            block[cp_itr] = block[bl_len+cp_itr];
          }
          bl_len = 0;
        }
        if(ci == '\n'){
//          handleGCodeLine(webserver.arg(0).substring(begining,i));
//          char c0 = webserver.arg(0)[begining];
          begining = i+1;
          bl_len += l_len;
          l_len = 0;
        }else if(ci == 'z' || ci == 'Z'){
          z_ind = i;
        }
      }
      block[bl_len] = '\0';
      Serial.println(block);
//      handleGCodeLine(webserver.arg(0).substring(begining));
    }
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", "OK");
  }else {
    webserver.send(405, "text/plain", "Method Not Allowed");
  }
}*/
void handleGCode(){
  if(webserver.method() == HTTP_POST){
    if(webserver.args() == 2 && webserver.argName(0) == "gcode"){
//     Serial.println(webserver.arg(0));
      int begining = 0;
      int len = webserver.arg(0).length();
      for(int i=0; i<len; i++){
        if(webserver.arg(0)[i] == '\n'){
          handleGCodeLine(webserver.arg(0).substring(begining,i));
          begining = i+1;
        }
      }
      handleGCodeLine(webserver.arg(0).substring(begining));
    }
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", "OK");
  }else {
    webserver.send(405, "text/plain", "Method Not Allowed");
  }
}
void handleFileUpload() {
  if (webserver.uri() != "/file/") {
    return;
  }
  HTTPUpload& upload = webserver.upload();
  if (upload.status == UPLOAD_FILE_START) {
    String filename = upload.filename;
    if (!filename.startsWith("/")) {
      filename = "/" + filename;
    }
    filename = String();
  } else if (upload.status == UPLOAD_FILE_WRITE) {
    //Serial.print("handleFileUpload Data: "); Serial.println(upload.currentSize);
    for(int i=0; i< upload.currentSize; i++){
      char c = upload.buf[i];
      file_data += c;
    }
  } else if (upload.status == UPLOAD_FILE_END) {
    file_data += "handleFileUpload Size: ";
    file_data += String(upload.totalSize);
  }
}
void handlePassCommands(){
  if (webserver.method() == HTTP_POST) {
    if(webserver.args() == 2 && webserver.argName(0) == "commands"){
      Serial.println(webserver.arg(0));
    }
    String s = Serial.readString();
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", s);
  } else {
    webserver.send(405, "text/plain", "Method Not Allowed");
  }
}
void handleAvailable(){
    int free_space = ESP.getFreeHeap();
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", "Yes"+String(free_space));
}
void handleNotFound() {
  /*if (webserver.method() == HTTP_OPTIONS)
    {
        webserver.sendHeader("Access-Control-Allow-Origin", "*");
        webserver.sendHeader("Access-Control-Max-Age", "10000");
        webserver.sendHeader("Access-Control-Allow-Methods", "PUT,POST,GET,OPTIONS");
        webserver.sendHeader("Access-Control-Allow-Headers", "*");
        webserver.send(204);
    }
    else*/
    {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += webserver.uri();
  message += "\nMethod: ";
  message += (webserver.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += webserver.args();
  message += "\n";
  for (uint8_t i = 0; i < webserver.args(); i++) {
    message += " " + webserver.argName(i) + ": " + webserver.arg(i) + "\n";
  }
  STDLOG.println(message);
  webserver.send(404, "text/plain", message);
  }
}
void handleDraw(){
  int free_before = ESP.getFreeHeap();
  int scale_x = 1;
  int scale_y = 1;
  if (webserver.method() == HTTP_POST) {
    String response = "Malfarmed stream";
    //----------------------------------------------------
/*    Serial.println(webserver.args());
    for(int i=0; i<webserver.args(); i++){
      Serial.print(webserver.arg(i));
      Serial.print(webserver.argName(i));
    }*/
    //----------------------------------------------------
    if(webserver.args() == 6 && webserver.argName(0) == "contour" && webserver.argName(1) == "scale_x" 
    && webserver.argName(2) == "scale_y" && webserver.argName(3) == "down" && webserver.argName(4) == "up"){
      scale_x = webserver.arg(1).toInt();
      scale_y = webserver.arg(2).toInt();
      int down = webserver.arg(3).toInt();
      int up = webserver.arg(4).toInt();
    int i;
    int len = webserver.arg(0).length();
    if(len % 4 == 0){
      for(i=0; i<len;){
        byte xl = webserver.arg(0)[i];
        byte xr = webserver.arg(0)[i+1];
        byte yl = webserver.arg(0)[i+2];
        byte yr = webserver.arg(0)[i+3];
        int x = xl*256+xr;
        int y = yl*256+yr;
        Serial.print("m ");
        Serial.print(x*scale_x);
        Serial.print(' ');
        Serial.println(y*scale_y);
        char c = waitNread();
        if(c == 'n'){
          response = "Could not reach"+String(x)+","+String(y);
          break;
        }
        if(i==0){
          Serial.println("p "+String(down));
        }
        i+=4;
      }
      Serial.println("p "+String(up));
      if(i == webserver.arg(0).length()){
        response = "OK";
      }
      }
    }else{
      response += (webserver.args() == 6);
      response += (webserver.argName(0) == "contour");
      response += (webserver.argName(1) == "scale_x");
      response += (webserver.argName(2) == "scale_y");
      response += String(webserver.args());
      response += webserver.argName(0);
      response += webserver.argName(1);
      response += webserver.argName(2);
    }
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", response+" "+String(free_before)+" "+String(ESP.getFreeHeap()));
  } else {
    webserver.send(405, "text/plain", "Method Not Allowed");
  }
}
void webserver_setup(){
  webserver.on("/blink/",handleBlink);
  webserver.on("/available/",handleAvailable);
  webserver.on("/pass_commands/",handlePassCommands);
  webserver.on("/draw/",handleDraw);
  webserver.on("/gcode/",handleGCode);
  webserver.on("/file/", HTTP_POST, []() {
  webserver.send(200, "text/plain", "file_data"+file_data);
  }, handleFileUpload);
  webserver.on("/set-system-mode/",setSystemMode);
//  webserver.on("/update-servo-pins/",updateServoPins);
  webserver.on("/servo-settings/",handleServoSystemSetting);
  webserver.on("/set-update-url/",setUpdateUrl);
  webserver.on("/update/",handleUpdate);
  webserver.on("/version/",handleVersion);
  webserver.onNotFound(handleNotFound);
  webserver.begin();
  STDLOG.println("HTTP server started");
  if(system_mode == 1){
    servo_system.init_servos();    
  }
}
void handle_client(){
  ensure_connect();
  webserver.handleClient();
}
/* ---------------------------------------------- Not used code ------------------------------------------------
  ---------------------------- webserver ---------------------------------------
  webserver.on("/moveto/", handleMoveTo);
  webserver.on("/displace/", handleDisplace);
  webserver.on("/pick/",handlePick);
  ------------------------------------------------------------------------------








void handlePostRequest(char command){
  if (webserver.method() == HTTP_POST) {
    if(webserver.args() == 1 && webserver.argName(0) == "plain"){
      Serial.print(command);
    }
    String s = Serial.readString();
    webserver.sendHeader("Access-Control-Allow-Origin","*");
    webserver.send(200, "text/plain", s);
  } else {
    webserver.send(405, "text/plain", "Method Not Allowed");
  }
}
void handleMoveTo() {
  handlePostRequest('m');
}
void handleDisplace() {
  handlePostRequest('d');
}
void handlePick() {
  handlePostRequest('p');
}

 */
