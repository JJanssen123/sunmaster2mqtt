#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3 as published by
#    the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details. <http://www.gnu.org/licenses/>.
#
#    Written in 2012 and 2020 by Jorg Janssen <http://www.zonnigdruten.nl/>

import socket
import struct
import time
import paho.mqtt.publish as publish
import json
from datetime import datetime, timedelta
from sm_comm import *
from settings import *


# BEGIN PROGRAM ----------------------------------------------

if (split_date_into_topics):
    date_format = '%Y/%m/%d'
else:
    date_format = '%Y-%m-%d'
    
def mqtt_publish(topic, message, retain):
    try:
        publish.single(topic=topic, payload=message, hostname=mqtt_broker, auth={'username':mqtt_username,'password':mqtt_password}, retain=retain)
    except:
        Debug('Mqtt publish failed: ' + str(sys.exc_info()[0]), 1)  

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s.settimeout(1)

    try:
        s.connect((TCP_IP, TCP_PORT)) # connect to tcp-converter
    except:
        Debug('Unable to connect to tcp converter: ' + str(sys.exc_info()[0]), 1)
        mqtt_publish(mqtt_base_topic,'Unable to connect to tcp converter', False)
    else:
        # "flush":
        while (1):
            try:
                chunk = s.recv(1) # block untill timeout
            except:
                # flushing done
                break

        # send the first command, to discover all connected inverters
        rq = RequestC1()
        rq.send(s)
        try:
            responses = Read(s)
        except:
            Debug('Error in reading responses: ' + str(sys.exc_info()[0]), 1)
            mqtt_publish(mqtt_base_topic, 'Error in reading responses', False)
        else:
            if(not responses):
                Debug('No responses', 2)
            else:
                # get inverters from response
                inverters = []
                for r in responses:
                    if (r.type == 193):
                        i = Inverter(r.address,s)
                        inverters.append(i)
                    else:
                        Debug('Response type does not match request C1', 1)                
                        
                # get values from inverters
                for i in inverters:
                    inverter_id = str(int.from_bytes(i.address[0:1],  byteorder='little', signed = False))                    

                    # get running values for this moment
                    i.getRunningValues()
                    params = {} 
                    for v in i.values:
                        params[v] = i.values[v] 
                    if (use_json):
                        mqtt_publish(mqtt_base_topic + '/' + inverter_id, json.dumps(params), True)
                    else:
                        for p in params:
                            mqtt_publish(mqtt_base_topic + '/' + inverter_id + '/' + p, str(params[p]), True)

                    # get daily values for today (d = 0)                          
                    i.getDailyValues(0) 
                    params = {}            
                    for v in i.dailyValues[0]:
                        params[v] = i.dailyValues[0][v] 
                    date = datetime.now().strftime(date_format)                            
                    if (use_json):
                        mqtt_publish(mqtt_base_topic + '/' + inverter_id + '/' + date, json.dumps(params), True)
                    else:
                        for p in params:
                            mqtt_publish(mqtt_base_topic + '/' + inverter_id + '/' + date + '/' + p, str(params[p]), True)   
   
                    # get other daily values, if not yet done today
                    try:
                        f = open('lastdate.' + inverter_id, 'r')
                        last_date = f.read()
                        f.close()
                    except:
                        last_date = ''                        
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    if(last_date != current_date):
                        for d in range(1,30): 
                            params = {} 
                            i.getDailyValues(d) 
                            for v in i.dailyValues[d]:
                                params[v] = i.dailyValues[d][v]
                            date = (datetime.now() - timedelta(d)).strftime(date_format)  
                            if (use_json):
                                mqtt_publish(mqtt_base_topic + '/' + inverter_id + '/' + date, json.dumps(params), retain_daily_messages)
                            else:
                                for p in params:
                                    mqtt_publish(mqtt_base_topic + '/' + inverter_id + '/' + date + '/' + p, str(params[p]), retain_daily_messages)   

                            f = open('lastdate.' + inverter_id, 'w')
                            f.write(current_date)
                            f.close()                
    s.close()

main()
# END PROGRAM ---------------------------------------------
