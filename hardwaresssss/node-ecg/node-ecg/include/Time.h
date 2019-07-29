#ifndef __TIME_H__
#define __TIME_H__

#include "Arduino.h"
#include "math.h"

class Time {
  private:
    int minute;
    int second;
    int millisecond;

  public:
    String getTime() {
      return String(millis());
    }

    // String getTime(){
    //   long ms = millis();
      
    //   millisecond = ms % 1000;
    //   second = (int) floor(ms / 1000) % 60;
    //   minute = (int) floor(ms / 1000 / 60) % 60;

    //   return ((minute < 10) ? '0' + String(minute) : String(minute)) + ':' +
    //          ((second < 10) ? '0' + String(second) : String(second)) + '.' +
    //          String(millisecond);
    // }
};

#endif