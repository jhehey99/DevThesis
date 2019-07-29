#ifndef __UTILS_H__
#define __UTILS_H__

#include "string.h"

// \ buffer used to store int converted to string
#define INT_SIZE    10
char int_buffer[INT_SIZE] = "";


// \ int to string
void itostr(int n) {
    snprintf(int_buffer, INT_SIZE, "%d", n);
}

#endif