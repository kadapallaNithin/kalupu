#ifndef arm_h
#include<Arduino.h>
#include<Servo.h>
#include "pin_map.h"
class Axis{
  char Name;
  int _pos;//position
  int _pin;
  int _dir_pin;
  float _steps_per_unit;
  int _delay;
  int _quick_delay;
  bool _quick_mode; // quick or normal i.e g0 or g1
  int _lower_limit;
  int _upper_limit;
public:
  Axis(){}
  Axis(char n, int pin, int dirPin, float steps, int u,int d=500,int pos=0,int l=0,int quick_delay=0);
  int getPosition();
  void setPosition(int pos);
  void setStepsPerUnit(float);
  float getStepsPerUnit();
  void setQuickMode(bool m){_quick_mode = m;}
  void setAttribute(char c,int value);
//  void get_limits(int& l,int& u);
//  void set_speed(int s){}
  bool moveTo(int p);
  void displace(int dist);
//  bool check_n_displace(int dist); // checks for limits
  bool can_move(int dist);
};

class Arm{
  Axis _x,_y,_z;
  char _mode;
//  Servo pick_servo;
public:
  Arm(Axis x,Axis y,Axis z,char mode='3');
  void getPosition(int& x, int& y, int& z);
  bool setMode(char mode);
  void setPosition(int x, int y, int z);
  void setAxisAttribute(char, char, int);
  void setAxisStepsPerUnit(char axis_name,float value);
  void setFeedRate(int f);
  void setQuickMode(bool m);
  void setQuickDelay(int );
  bool displace(int x,int y);
//  bool serialMoveTo(int x=0,int y=0, int z=0);
  bool rotateTo(int x);
  bool moveTo(int x, int y); // x,y in steps move axes parallelly
  bool moveTo(float x,float y);// x,y in units
  bool moveZ(float z);
  void circle(int r);
};
extern Arm a;
extern Axis y_axis;
extern Servo pick_servo;
extern int pick_servo_position;
#endif
