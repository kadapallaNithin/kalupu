#ifndef nithin_servo_h
#define nithin_servo_h 1 
#include <Servo.h>
#define NUMBER_OF_SERVOS 3
#include <ArduinoJson.h>
extern Servo s[NUMBER_OF_SERVOS];
extern int number_of_servo_data_objects;
extern String file_data;
class ServoData{
  int i;
  int servo_pin;//s[NUMBER_OF_SERVOS] = {14,14,14};
  int pos;//itions[NUMBER_OF_SERVOS] = {180,180,180};
  int up_angle;//[NUMBER_OF_SERVOS] = {160,160,160};
  int down_angle;//[NUMBER_OF_SERVOS] = {180,180,180};
  public:
  ServoData(){
    i = number_of_servo_data_objects; number_of_servo_data_objects++;
  }
//  ServoData(int ind,int pin, int posi, int up_ang, int down_ang){ i=ind,servo_pin = pin;pos = posi;up_angle = up_ang;down_angle = down_ang; }
  void set_servo_pin(int pin) { servo_pin = pin; }
  int get_servo_pin()         { return servo_pin; }
  void set_position(int posi) { pos = posi; }
  void rotateTo(int angle);
  void up(){ rotateTo(up_angle); }
  void down(){ rotateTo(down_angle); }
  void toJsonObject(JsonObject obj);
  bool fromJsonObject(JsonObject obj);
  void init(){ s[i].attach(14); }
  void sweep();
};
class ServoSystem{
  ServoData servo_data[NUMBER_OF_SERVOS];
  public:
  void sweep(int i);
  void init_servos();
  String get_settings();
  bool set_settings(String json);
  void down(int i){ servo_data[i].down(); }
  void up(int i){ servo_data[i].up(); }
};
extern ServoSystem servo_system;
#endif
