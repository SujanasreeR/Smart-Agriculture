#****Internet of things******#
#****Final Project****#
#**Submitted By Group 10**#
# Pooja Shrivastava & Sujana Ratakonda #

#libraries to install for the project

import json
import time
from grovepi import *
import paho.mqtt.client as mqtt
import grovepi
from grove_rgb_lcd import *
from grovepi import*

#Initialize sensors digital Port for our code#

th_sensor = 3 # digital port D3
led = 4 # digital port D4
moist_sensor = 0 # analog port A0
light_sensor = 1 #analog port A1
relay = 8 # digital port D8
threshold = 10 #threshold of resistance for light sensor.. 

# IBM Watson IoT Platform connection details...

host = '8k7yaw.messaging.internetofthings.ibmcloud.com' #IBM watson host ID
clientid='d:8k7yaw:Sensors:SoilSensors'    #Client id indicates the Device type and name of the device#
username='use-token-auth'  #it is default for MQTT
password='EZ&Actirkx_N+Nx+-b'  #it is the authentication code 
topic='iot-2/evt/temperature/fmt/json' #it is the topic associated with the MQTT
topic1='iot-2/evt/led/fmt/json'  #it will display the led on watson
topic2='iot-2/evt/moist_sensor/fmt/json'  #it will display moisture sensor value on watson
topic3='iot-2/evt/light_sensor/fmt/json'  #it will display light sensor on watson
topic4='iot-2/evt/light_status/fmt/json'  #it will display the light status on watson
topic5='iot-2/evt/led_status/fmt/json'   #it will display the led status on watson

#connection to IBM Watson IoT platform server

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
client.connect(host, 1883, 60)
count = 0

#pin mode

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(relay, "OUTPUT")
grovepi.pinMode(led, "OUTPUT")

#Program Starts taking the sensor reading from here....

count = 0

while (1):
 
 try:
  # begin reading temperature and humidity
  [temp,hum] = dht(th_sensor, 0) #temperature & humidity
  client.publish(topic, json.dumps({'Temperature': temp, 'Humidity':hum})) #Publishes on Watson plaform
  time.sleep(.5)
 
  # begin reading light sensitivity ...
  light = (grovepi.analogRead(light_sensor))
  print ("light sensivitivty is %s" %light)
  resistance = (float)(1023 - light) * 10 / (light+1)
  time.sleep(.5)

 #print values on console for light, temperature & humidity....
  print ("light = %d resistance = %.2f" %(light, resistance))
  print ('temp: ' + str(temp) + '\t' + 'Humidity: ' + str(hum))
  setText("Temperature = %s & Humidity = %s" % (temp, hum))
  
  try:
        if resistance < threshold: #for light sensor value
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
            light_status = "It is now sunrise!!" #display on watson gauges...
            led_status = "Need some water....!!" #display when led is on..
            print ("It is now sunrise!")  
            print ("Need some water....!!") 
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)
            light_status = "It is sunset time" #display on watson gauges..
            led_status = "No need to water plant...!!" #pump off, display on gauge..
            print ("It is sunset time")  
            print ("No need to water plant...!!")

      #Real time update on IBM Watson gauges.... 
        client.publish(topic1, json.dumps({'LED': led}))
        client.publish(topic4, json.dumps({'Light': light_status}))
        client.publish(topic3, json.dumps({'Light': light}))
        client.publish(topic5, json.dumps({'LED': led_status}))
		

  except IOError:
        print ("An Error has occured")
  
  time.sleep(0.5) #wait for .5 sec after displaying temperature & humidity
  moist = (grovepi.analogRead(moist_sensor)) #read moisture from sensor
  client.publish(topic2, json.dumps({'Moisture': moist})) #publish real time data on watson..
  print ('moisture: '+ str(moist))  #moisture value..
  setText("Moisture = %s" %(moist))  #display moisture value on LCD
  setRGB(0,128,64) #Blue color

  if (moist < 400): #check the moist value range
    digitalWrite(relay,1) #Moisture <400 Pump on
    setRGB(30,255,30) #LCD turns Green
    setText("Temperature = %s & Humidity = %s" % (temp, hum)) #Display real time on LCD
    setText("Moisture = %s" %(moist)) #Display real time on LCD
    time.sleep(5) #sleep for 5 seconds
    digitalWrite(relay,0) #Pump turns off after 5 seconds of sleep
    setRGB(255,30,30)   #LCD turns red 
    
  else:
    digitalWrite(relay,0) 
    setText("Temp = %s & Hum = %s & Mois = %d" % (temp, hum, moist))  #Display real time on LCD
    time.sleep(5) #sleep for 5 seconds
    setText("Moisture = %s" %(moist))  #Display real time on LCD
            
 except Exception as ex:
  print ('An error has occured: %s' % ex)

client.loop()
client.disconnect()

   


