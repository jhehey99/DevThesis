#ifndef __JSONBUILDER_H__
#define __JSONBUILDER_H__

#include "Arduino.h"

class JsonBuilder {
    
    private: 
       /* Header */
        const String initialHeader = "\"header\":[]";
        int headerCount;
        String header;

        /* Data */
        const String initialData = "\"data\":{";
        int dataCount;
        String data;

        /* Times */
        const String initialTimes = "\"times\":[]";
        String times;

        /* Values */
        const String initialValues = "\"values\":[]";
        String values ;

    public: 
        JsonBuilder() {
            clear();
        }

        /* [ {key[0] : [datas[0]]}, ...] */
        /* [ {"times" : ["00:00", "00:01", ...]}, {"values" : ["12", "13", ...]}] */
        void addData(String time, String value) {
            
            // add quotes
            time = "\"" + time + "\"";
            value = "\"" + value + "\"";

            if(dataCount > 0) {
                time = ',' + time;
                value = ',' + value;
            }

            // remove last characters ']'
            times.remove(times.length() - 1);
            values.remove(values.length() - 1);

            // append time and value
            times += time + ']';
            values += value + ']';
            
            dataCount ++;
        }

        String getJson() {
            // return "{" + header + "," + data + times + "," + values + "}}~";
            return "{" + data + times + "," + values + "}}~";
        }

        void clear() {
            header = initialHeader;
            data = initialData;
            times = initialTimes;
            values = initialValues;
            headerCount = 0;
            dataCount = 0;
        }


        int getBodyCount() {
            return dataCount;
        }

        int getHeaderCount() {
            return headerCount;
        }
};



#endif