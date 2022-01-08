#include "arm.h"
#define X_STEPS 200
#define Y_STEPS 200
#define Z_STEPS X_STEPS
Axis y_axis = Axis('y',Y_AXIS_PIN,Y_DIR_PIN,Y_STEPS,1000,100);
Arm a = Arm(Axis('x',X_AXIS_PIN,X_DIR_PIN,X_STEPS,1000,100),y_axis,Axis('z',Z_AXIS_PIN,Z_DIR_PIN,Z_STEPS,1000));
Servo pick_servo;
int pick_servo_position = 150;
Axis::Axis(char n,int pin, int dir_pin, float steps, int u,int d=500,int pos=0,int l=0,int quick_delay=0){
    Name = n;
    _pos = pos;//position
    _pin = pin;
    _dir_pin = dir_pin;
    _steps_per_unit = steps;
    _delay = d;
    if(quick_delay == 0){
      _quick_delay = d;
    }else{
      _quick_delay = quick_delay;      
    }
     _quick_mode = false;
    _lower_limit = l;
    _upper_limit = u;
    pinMode(_pin,OUTPUT);
    pinMode(_dir_pin,OUTPUT);    
}
int Axis::getPosition(){
    return _pos;
}
void Axis::setPosition(int pos){
  _pos = pos;
}
void Axis::setStepsPerUnit(float value){
  _steps_per_unit = value;
}
float Axis::getStepsPerUnit(){
  return _steps_per_unit;
}
void Axis::setAttribute(char attribute,int value){
   if(attribute == 'd'){
     if(value > 0){
       _delay = value;
     }
   }else if(attribute == 'q'){
     if(value > 0){
       _quick_delay = value;
     }
   }
}
/*void Axis::get_limits(int& l,int& u){
  l = _lower_limit;
  u = _upper_limit;
}*/
bool Axis::can_move(int dist){
  return true;//_lower_limit <= _pos + dist && _pos + dist < _upper_limit;
}
//  void set_speed(int s){}
void Axis::displace(int dist){ // dist in steps
//  Serial.println(Name);
  _pos += dist;
  if(dist < 0){
    digitalWrite(_dir_pin,LOW);
    dist *= -1;
  }else{
    digitalWrite(_dir_pin,HIGH);
  }
  int steps_to_move = dist;//*_steps_per_unit;
  int d;
  if(_quick_mode){
    d = _quick_delay;
  }else{
    d = _delay;
  }
  for(int i=0; i<steps_to_move; i++){
    digitalWrite(_pin,HIGH);
    delayMicroseconds(d);
    digitalWrite(_pin,LOW);
    delayMicroseconds(d);
  }
}
/*bool Axis::check_n_displace(int dist){
  if(can_move(dist)){
    displace(dist);
    return true;
  }
  return false;
}*/
bool Axis::moveTo(int p){
//  if(_lower_limit <= p && p < _upper_limit){
    int dist = p - _pos;
    displace(dist);
    return true;
  //}
  return false;
}
Arm::Arm(Axis x,Axis y,Axis z,char mode='3'){
    _x = x;
    _y = y;
    _z = z;
    _mode = mode;
}
void Arm::getPosition(int& x, int& y, int& z){
    x = _x.getPosition();
    y = _y.getPosition();
    z = _z.getPosition();    
}
bool Arm::setMode(char mode){
  _mode = mode;
}
void Arm::setPosition(int x, int y, int z){
  _x.setPosition(x);
  _y.setPosition(y);
  _z.setPosition(z);
}
void Arm::setAxisAttribute(char axis_name,char attribute, int value){
   Axis* axis;
   if(axis_name == 'x'){
     axis = &_x;
   }else if(axis_name == 'y'){
     axis = &_y;
   }else if(axis_name == 'z'){
     axis = &_z;
   }
   axis->setAttribute(attribute,value);
}
void Arm::setAxisStepsPerUnit(char axis_name,float value){
   Axis* axis;
   if(axis_name == 'x'){
     axis = &_x;
   }else if(axis_name == 'y'){
     axis = &_y;
   }else if(axis_name == 'z'){
     axis = &_z;
   }
   axis->setStepsPerUnit(value);  
}
void Arm::setFeedRate(int fr){
  _x.setAttribute('q',fr);
  _y.setAttribute('q',fr);
}
void Arm::setQuickMode(bool m){
  _x.setQuickMode(m);
  _y.setQuickMode(m);
}
bool Arm::displace(int x,int y){// x,y in steps
  if(!_x.can_move(x) || !_y.can_move(y)){
    return false;
  }
  if(x == 0){
    _y.displace(y);
    return true;
  }
  if(y == 0){
    _x.displace(x);
    return true;
  }
  Axis* slower = &_y;
  Axis* faster = &_x;
  int my_x = x;
  float slope = float(y)/x;
/*  if(x > y){
    Serial.println("Swap");
    slower = &_x;
    faster = &_y;
G0 X6.0383 Y6.4231
    my_x = y;
    slope = float(x)/y;
  }*/
  //Serial.println(slope);
  int dir = 1;
  if(my_x < 0){
    my_x *= -1;
    dir = -1;
    slope *= -1;
  }
  for(int i=1,j=0; i<=my_x;i++){
//    Serial.println(j);
    faster->displace(dir);
    int j_diff = slope*i-j;
    //Serial.print(j_diff);
    //Serial.print(',');
    slower->displace(j_diff);
    j = slope*i;
    //Serial.println(j);
  }
  return true;
}
bool Arm::rotateTo(int angle){
  int dir = 1;
  if(pick_servo_position > angle){
    dir = -1;
  }
//  Serial.println(pick_servo_position);
  while(pick_servo_position != angle){
    pick_servo_position += dir;
    pick_servo.write(pick_servo_position);
    delay(15);
  }
}
bool Arm::moveTo(int x,int y){// x,y in steps
  int px,py,pz;
  getPosition(px,py,pz);
  return displace(x-px,y-py);
}
bool Arm::moveTo(float x,float y){// x,y in units
  int px,py,pz;
  getPosition(px,py,pz);
  int dx = x*_x.getStepsPerUnit(),dy = y*_y.getStepsPerUnit();
  return displace(dx-px,dy-py);
}
bool Arm::moveZ(float z){
  if(_mode == '2'){//2d Mode
    if(z == 2){
      rotateTo(180);
    }else{
      rotateTo(160);
    }
  }else{
    Serial.println(z);
    _z.moveTo(z*_z.getStepsPerUnit());
  }
}
void Arm::circle(int radius){
  int prev_j = 0;
  int j;
  float ratio = _y.getStepsPerUnit()/_x.getStepsPerUnit();
  for(int i=-radius; i<=radius; i++){
    float x  = sqrt(radius*(long)radius-i*(long)i)*ratio;
    j = x;
//    Serial.println(j);
    _x.displace(1);
    //displace(1,j-prev_j);
    _y.displace(j-prev_j);
//  Serial.print(j);
  //Serial.println(j-prev_j);
    prev_j = j;
  }
  for(int i=radius; i>=-radius; i--){
    j = sqrt(radius*(long)radius-i*(long)i)*ratio;
    _x.displace(-1);
    //displace(1,j-prev_j);
    _y.displace(prev_j-j);
//  Serial.print(j);
  //Serial.println(j-prev_j);
    prev_j = j;
  }
}
