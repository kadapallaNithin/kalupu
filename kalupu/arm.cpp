/*#include "arm.h"
#define X_STEPS 200
#define Y_STEPS X_STEPS
#define Z_STEPS X_STEPS
Arm a = Arm(Axis(),Axis(),Axis());
Axis::Axis(int pin, int steps, int u,int l=0,int pos=0,int d=500){
    _pos = pos;//position
    _pin = pin;
    _steps_per_unit = steps;
    _delay = d;
    _lower_limit = l;
    _upper_limit = u;
 }
int Axis::getPosition(){
    return _pos;
}
//  void set_speed(int s){}
bool Axis::moveTo(int p){
    if(_lower_limit <= p && p < _upper_limit){
      int dist = p - _pos;
      int steps_to_move = dist*_steps_per_unit;
      for(int i=0; i<steps_to_move; i++){
          digitalWrite(_pin,HIGH);
        delayMicroseconds(_delay);
        digitalWrite(_pin,LOW);
        delayMicroseconds(_delay);
      }
      return true;
    }
    return false;
}
Arm::Arm(Axis x,Axis y,Axis z){
    _x = x;
    _y = y;
    _z = z;
}
void Arm::getPosition(int& x, int& y, int& z){
    x = _x.getPosition();
    y = _y.getPosition();
    z = _z.getPosition();    
}
bool Arm::serialMoveTo(int x,int y, int z){ // give default for z
    return _x.moveTo(x) && _y.moveTo(y) && _z.moveTo(z);        
}
// bool moveTo(){} // move axes parallelly*/
