import paho.mqtt.client as mqtt

import paho.mqtt.publish as publish

import androidhelper

import time



#Here goes your broker IP/Address and port, username, and password if appliable
def on_message(client,userdata,message):
   mess=message.payload.decode('utf-8')
   print(mess)
   mobid='jasmine'
   if mess[0]=='m':
       msg='false'
       print("entered")
       while(msg!='true'):
           print("entered")
           droid1=androidhelper.Android()
           droid1.dialogGetPassword("please enter your password","Confirm your identity")
           result=	droid1.dialogGetResponse().result
           ans=result.get("value")
           print(ans) 
           mobid='jasmine'
           if(ans==mobid):
               msg='true'
               publish.single('result',msg,qos=2,hostname='m16.cloudmqtt.com',port=17679,auth={'username':'mtpelhgh','password':'pxF6nKV4sShm'})
               client.disconnect()
               client.loop_stop()                     
   publish.single('result','true',qos=2,hostname='m16.cloudmqtt.com',port=17679,auth={'username':'mtpelhgh','password':'pxF6nKV4sShm'})
   client.disconnect()
   client.loop_stop()


# MQTT initialzation

broker='m16.cloudmqtt.com'

broker_port=17679

user='mtpelhgh'

passwd='pxF6nKV4sShm'

#Just a name to identify the runner, vehicle...

mobile_id = 'jasmine'
mqtt_client = mqtt.Client()

mqtt_client.username_pw_set(user,passwd)
mqtt_client.connect(broker,broker_port)

#Android initialization


droid = androidhelper.Android()

point_id=0
while True:
   droid.startLocating()
   droid.batteryStartMonitoring()
   time.sleep(120)
   loc = droid.readLocation()[1]
   lat = 0

   lon = 0
   batterylevel= droid.batteryGetLevel()

   if loc != {}:

      try:
           data = loc['gps']
           source='GPS'
      except KeyError:
           data = loc['network']
           point_id +=1
           source='NETWORK'
      timestamp=int(time.time())
      lat = data['latitude'] 
      lon = data['longitude']
      wifi1r=0
      wifi2r=0
      wifi1s=0
      wifi2s=0
      Gsent=0
      Grecv=0
      count=0
      runningapps=droid.getRunningPackages()[1]
      for i in runningapps:
         if "android" not in i:
              count=count+1
      display=droid.getScreenBrightness()[1]
      batterylevel=droid.batteryGetLevel()[1]
      ischarging=droid.batteryGetStatus()[1]
      networkstatus=droid.getNetworkStatus()
      msg = '{"tid":%s,"tst:"%s,"lat":%s,"lon":%s,"wifi1r:"%s,"wifi1s:"%s,"wifi2r:"%s,"wifi2s:"%s,"3Gsent:"%s,"3Grecv:"%s,"runningapps:"%s,displayon:"%s,batterylevel":%s,"ischarging:"%s}'%(mobile_id, timestamp,lat, lon,wifi1r,wifi1s,wifi2r,wifi2s,Gsent,Grecv,count,display,batterylevel,ischarging)
      try:
            mqtt_client.connect(broker,broker_port)

            publish.single('phone data',msg,qos=2,hostname=broker,port=broker_port,auth={'username':user,'password':passwd})
            print ('DATA SENT->',source,msg)
            mqtt_client.disconnect()
            mqtt_client.connect(broker,broker_port)
            mqtt_client.loop_start()
            mqtt_client.subscribe('malicious',qos=1)
            mqtt_client.on_message=on_message
     
      except Exception as e:
            print (e, "Error while connecting to MQTT broker")

   else:
       print ("Location not available. Check your device settings")
   droid.stopLocating()
   droid.batteryStopMonitoring


