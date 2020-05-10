# YOUR SETTINGS HERE -----------------------------------------

TCP_IP = '192.168.1.6'  # ip address of rs485-to-tcp converter
TCP_PORT = 23           # tcp port of this converter

mqtt_broker = "localhost" 
mqtt_username = "xxx"  
mqtt_password = "xxx"
mqtt_base_topic = "domotica/sunmaster" # this is appended with /inverter_id for each inverter

use_json = True # True publishes all data in one topic in a json string, False means each attribute is published as separate topic
split_date_into_topics = False # True splits the date into /year/month/day topics, False publishes data as one topic: /year-month-day
retain_daily_messages = True # True sends retain flag with mqtt messages containing daily production data for past 30 days

debug_level = 1 # 0 = no debug messages at all, 1 = only errors, 2 = informative and errors

# END OF SETTINGS --------------------------------------------
