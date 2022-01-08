/*#ifndef arm_h
#include<Arduino.h>
#include "pin_map.h"
class Axis{
  int _pos;//position
  int _pin;
  int _steps_per_unit;
  int _delay;
  int _lower_limit;
  int _upper_limit;
public:
  Axis(){}
  Axis(int pos,int pin, int steps,int d, int l, int u);
  int getPosition();
//  void set_speed(int s){}
  bool moveTo(int p);
};

class Arm{
  Axis _x,_y,_z;
public:
  Arm(Axis x,Axis y,Axis z);
  void getPosition(int& x, int& y, int& z);
  bool serialMoveTo(int x=0,int y=0, int z=0);
  // bool moveTo(){} // move axes parallelly
};
extern Arm a;
#endif*/
