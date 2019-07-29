#ifndef __JSONBUILDER_H__
#define __JSONBUILDER_H__

#include "Arduino.h"

class JsonBuilder {
    
    private: 
       /* Header */
        const String initialHeader = "\"header\":[\n]";
        int headerCount;
        String header;

        /* Body */
        const String initialBody = "\"body\":[\n]";
        int bodyCount;
        String body;

    public: 
        JsonBuilder() {
            clear();
        }

        /* { "key" : "keyStr", "value" : "valueStr" } */
        void addBody(String keyStr, String valueStr) {
            addBody("key", keyStr, "value", valueStr);
        }

        /* { "key" : "keyStr", "value" : "valueStr" } */
        void addBody(String key, String keyStr, String value, String valueStr) {
            // build json string
            String jsonBody = "{\"" + key + ":\":\"" + keyStr + "\", \"" + value + "\":\"" + valueStr + "\"}\n";

            // lagyan ng ',' sa unahan
            if(bodyCount > 0) {
                jsonBody = ',' + jsonBody;
            }

            // remove last character
            int len = body.length();
            body.remove(len-1);

            // append string to body
            body = body + jsonBody + ']';
            bodyCount ++;
        }

        String getJson() {
            return "{\n" + header + ",\n" + body + "\n}";
        }

        void clear() {
            header = initialHeader;
            body = initialBody;
            headerCount = 0;
            bodyCount = 0;
        }


        int getBodyCount() {
            return bodyCount;
        }

        int getHeaderCount() {
            return headerCount;
        }
};



#endif