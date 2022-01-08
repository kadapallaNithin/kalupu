#include "servo.h"
ServoSystem servo_system;
Servo s[3];
int number_of_servo_data_objects = 0;
void ServoData::rotateTo(int angle){
    int dir = 1;
    if(pos > angle){
      dir = -1;
    }
    while(pos != angle){
      pos += dir;
      s[i].write(pos);
      delay(15);
    }
}
bool ServoData::fromJsonObject(JsonObject obj){
  JsonVariant v;
  /*v = obj["i"];
  if(!v.isNull()){
    i = v.as<int>();
  }*
  v = obj["servo_pin"];
  if(!v.isNull()){
    servo_pin = v.as<int>();
    s[i].attach(servo_pin);
  }*/
  v = obj["pos"];
  if(!v.isNull()){
    pos = v.as<int>();
    s[i].write(pos);
    delay(1000);
  }
  v = obj["up_angle"];
  if(!v.isNull()){
    up_angle = v.as<int>();
  }
  v = obj["down_angle"];
  if(!v.isNull()){
    down_angle = v.as<int>();
  }
  return true;
}
void ServoData::sweep(){
/*  for(int ang=0; ang<180; ang++){
    s[i].write(ang);
    delay(15);
  }
  for(int ang=180; ang>0; ang--){
    s[i].write(ang);
    delay(15);
  }*/
  rotateTo(180);
  rotateTo(0);
}
void ServoData::toJsonObject(JsonObject obj){
  obj["i"] = i;
  obj["servo_pin"] = servo_pin;
  obj["pos"] = pos;
  obj["up_angle"] = up_angle;
  obj["down_angle"] = down_angle;
}
void ServoSystem::init_servos(){
    for(int i=0; i<NUMBER_OF_SERVOS; i++){
      servo_data[i].init();
    }
}
String ServoSystem::get_settings(){
    DynamicJsonDocument doc(1024);
//    JsonArray settings = doc.to<JsonArray>(); // seem to create duplicates
    for(int i=0; i<NUMBER_OF_SERVOS; i++){
      JsonObject servo_obj = doc.createNestedObject();
      servo_data[i].toJsonObject(servo_obj);
//      settings.add(servo_obj);
    }
    String ret;
    serializeJson(doc, ret);
    return ret;
}
void ServoSystem::sweep(int i){
  servo_data[i].sweep();
}
bool ServoSystem::set_settings(String json){
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, json);
    if (error) {
  //    Serial.println(error.f_str());
      return false;
    }
    JsonArray arr = doc.as<JsonArray>();
    int len = arr.size();
    for(int i=0; i<len; i++){
      JsonObject servo_i = arr[0].as<JsonObject>();
      int index = servo_i["i"];
      if(!servo_data[index].fromJsonObject(servo_i)){
        return false;
      }
    }
    /*
    int i=0;
    for(JsonVariant value:arr){
      positions[i++] = value;
    }
    arr = doc["up"].as<JsonArray>();
    i = 0;
    for(JsonVariant value:arr){
      up_angle[i++] = value;
    }
    i = 0;
    arr = doc["down"].as<JsonArray>();
    for(JsonVariant value:arr){
      down_angle[i++] = value;
    }*/
    return true;
}
