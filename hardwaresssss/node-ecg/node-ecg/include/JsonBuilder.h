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
        const String initialData = "{\"data\":[";
        int dataCount;
        String data;


    public: 
        JsonBuilder() {
            clear();
        }

        /* {"data":["9372,904","9899,183",...]} */
        void addData(String entry) {
            entry = "\"" + entry + "\"";
            if(dataCount > 0) {
                entry = ',' + entry;
            }
            data += entry;
            dataCount ++;
        }

        void endData() {
            data += "]}~";
        }

        const String& getJson() {
            return data ;
        }

        void clear() {
            header = initialHeader;
            data = initialData;
            headerCount = 0;
            dataCount = 0;
        }

        const int getBodyCount() {
            return dataCount;
        }

        const int getHeaderCount() {
            return headerCount;
        }

        const int getDataLength() {
            return data.length();
        }
};



#endif