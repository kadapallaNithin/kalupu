/*const int xstepPin = 2;//2;//D4=2
const int ystepPin = 3;
const int xdirPin = 5;//D1
const int ydirPin = 6;*/
#include "arm.h"
void setup() {
  Serial.begin(115200);
  pick_servo.attach(11);
  pick_servo.write(pick_servo_position);
/*  pinMode(xstepPin,OUTPUT);
  pinMode(xdirPin,OUTPUT);
  pinMode(ystepPin,OUTPUT);
  pinMode(ydirPin,OUTPUT);*/
  //  pinMode(LED_BUILTIN,OUTPUT);
}
/*void move_axis(int stepPin,int steps,int dirPin,int step_delay){
  bool dir = true;
  if(steps < 0){
    dir = false;
    steps *= -1;
  }
  digitalWrite(dirPin,dir);
  for(int x= 0; x<steps; x++){
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(step_delay);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(step_delay);
  }
}*/
class GRBLController{
  uint8_t _status;
  Arm* _arm;
//  char* _status_codes[3] = {"OK","X not defined","Y not defined"};
  public:
    GRBLController(Arm* a){
      _status = 0;
      _arm = a;
    }
    bool parseFloatAfterChar(String s,char c, float& value){
      int START = s.indexOf(c);
      if (START < 0){
        return false;
      }
      value = s.substring(START + 1).toFloat();
      return true;
    }
    bool parseIntAfterChar(String s, char c, int& value){
      int START = s.indexOf(c);
      if (START < 0){
        return false;
      }
      value = s.substring(START + 1).toInt();
      return true;      
    }
    void extract_xyzf(String INPUT_STRING,float& x, float& y,float& z, int& f){
      _status = 0;
      if(parseFloatAfterChar(INPUT_STRING,'X',x)){
        _status += 1;
      }
      if(parseFloatAfterChar(INPUT_STRING,'Y',y)){
        _status += 2;
      }
      if(parseFloatAfterChar(INPUT_STRING,'Z',z)){
        _status += 4;
      }
      if(parseIntAfterChar(INPUT_STRING,'F',f)){
        _status += 8;
      }
    }
    void handleG00(String INPUT_STRING){
/*      float x,y,z;
      int f;
      extract_xyzf(INPUT_STRING,x,y,z,f);
      if(_status&1 && _status&2){
        _arm->moveTo(x,y);
      }
      if(_status&4){
        _arm->moveZ(z);
      }*/
      handleG01(INPUT_STRING);
    }
    void handleG01(String INPUT_STRING){
      float x,y,z;
      int f;
      extract_xyzf(INPUT_STRING,x,y,z,f);
      if(_status&8){
        _arm->setFeedRate(f);
      }
      if(_status& 0x1 && _status& 0x2){
        _arm->moveTo(x,y);
      }
      if(_status&4){
        _arm->moveZ(z);
      }
    }
    void handleCommand(){
      String INPUT_STRING = Serial.readStringUntil('\n');
      INPUT_STRING.toUpperCase();
      int command_code = INPUT_STRING.toInt();
      if(command_code == 1){
        _arm->setQuickMode(true);
        handleG01(INPUT_STRING);
      }else if (command_code == 0) {
        _arm->setQuickMode(false);
        handleG00(INPUT_STRING);
      }
//      Serial.println(_status_codes[_status]);
      Serial.print("ok\n");
    }
};
GRBLController g = GRBLController(&a);
void loop() {
  if(Serial.available() > 0){
    char command = Serial.read();
//    Serial.print("command ");
  //  Serial.println(command);
    /*
     * c    circle
     * d    displace
     * G,g  GRBL
     * ?M, ?m Grbl miscellanious
     * t    moveTo
     * r    rotate // previously pick
     * P    position
     * s    setting -see subcommands in the else if block
    */
    if(command == 'G' || command == 'g'){// GRBL command
      g.handleCommand();
    }else if(command == 'd'){
      //    bool moves = false;
      int x = 0 ,y = 0 ,z = 0;
      x = Serial.parseInt();
      y = Serial.parseInt();    
//    z = Serial.parseInt();
//    y_axis.displace(y);
      if(a.displace(x,y)){
        Serial.print("y");
      }else{
        Serial.print("n");
      }
    }else if(command == 't'){
      float x = 0,y = 0,z = 0;
      x = Serial.parseFloat();
      y = Serial.parseFloat();
      //z = Serial.parseInt();
      if(a.moveTo(x,y)){
        Serial.print("y");
      }else{
        Serial.print("n");
      }
    }else if(command == 'r'){// rotate
      int angle;
      angle = Serial.parseInt();
      a.rotateTo(angle);
      delay(15);
//      a.rotateTo(150);
    }else if(command == 'P'){// Position
      int x,y,z;
      a.getPosition(x,y,z);
      Serial.print(x);
      Serial.print(',');
      Serial.print(y);
      Serial.print(',');
      Serial.println(z);
    }else if(command == 'c'){
      int r = Serial.parseInt();
      a.circle(r);
    }else if(command == 's'){//setting or configuration
      
      while(!Serial.available());
      char sub_command = Serial.read();
      /*
       * p    position
       * a    axis
       * s    steps_per_unit
       * m    mode
      */
      if(sub_command == 'p'){//position
        int x = Serial.parseInt();
        int y = Serial.parseInt();
        int z = Serial.parseInt();
        a.setPosition(x,y,z);
      }else if(sub_command == 'a'){ //axis setting
        Serial.println("axis setting");
        char axis_name = Serial.read();
        char attribute = Serial.read();
        if(attribute == 's'){// steps_per_unit
          float stps = Serial.parseFloat();
          Serial.println(stps);
          
        }
      }else if(sub_command == 'm'){
        char mode = Serial.read();
        Serial.print("mode set:");
        Serial.println(mode);
        a.setMode(mode);
      }
    }
  }
}
