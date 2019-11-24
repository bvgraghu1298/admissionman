import csv
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import ast
import pandas as pd
from sklearn import svm, metrics,preprocessing
from sklearn.preprocessing import MinMaxScaler
import array
import psycopg2

wifi1r=0
wifi1s=0
wifi2r=0
wifi2s=0
Gsent=0
Grecv=0
runningapps=0
displayon=0
batterylevel=0
ischarging=0
        
def mqttconn(username,upasswd,port,usermqtt,passwrd):        
    print("script running")
    mqtt_client = mqtt.Client()
    #Here goes your broker IP/Address and port, username, and password if appliable
    broker='m16.cloudmqtt.com'
    broker_port=port
    user=usermqtt
    passwd=passwrd
    #Connection
    mqtt_client.username_pw_set(user,passwd)
    mqtt_client.connect(broker,broker_port)

    #The topic for the data will be TRACK but use what you want; must match the DEVICE script topic
    mqtt_client.subscribe([('phone data',2),('result',2)])
    mqtt_client.on_message=on_message
    mqtt_client.loop_forever()
    return

def on_message(client, userdata, message):
    global mqttuser  
    global mqttpass
    global port
    global username  
    global wifi1r
    global wifi1s
    global wifi2r
    global wifi2s
    global Gsent
    global Grecv
    global runningapps
    global displayon
    global batterylevel
    global ischarging
    broker='m16.cloudmqtt.com'
    broker_port=port
    user=mqttuser
    passwd=mqttpass
    usernam=username
    path='C:\\Users\\jasmine.wadhwania\\Desktop\\%s.csv'%(usernam)     
    messaged=message.payload.decode("utf-8")
    if messaged[0]=='{':
        print("entered")
        data = pd.read_csv(path, sep = ";")
        arr = data.values
       
        print(arr)
        x = arr[:,3:15]
        X= preprocessing.normalize(x)
        print(X)
        y = arr[:,15]
        y = y.astype('int')

        X_train = X[16:]
        X_test = X[:15]
        y_train = y[16:]
        y_test = y[:15]

        
        model = svm.SVC()
        model.fit(X_train,y_train)
        model.score(X_test,y_test)

        print("recieved ",message.payload.decode("utf-8"))
        
        messagec=messaged.strip('{')
        messagec=messagec.strip('}')
        messagec=messagec.split(',')
        tid=messagec[0][6: ]
        tst=messagec[1][6: ]
        lat=messagec[2][6: ]
        lon=messagec[3][6: ]
        wifi1r=int(messagec[4][9: ])
        wifi1s=int(messagec[5][9: ])
        wifi2r=int(messagec[6][9: ])
        wifi2s=int(messagec[7][9: ])
        Gsent=int(messagec[8][9: ])
        Grecv=int(messagec[9][9: ])
        runningapps=int(messagec[10][14: ])
        displayon=int(messagec[11][11: ])
        batterylevel=int(messagec[12][14: ])
        ischarging=int(messagec[13][13: ])
        
        '''datatopredict=[5,6,wifi1r,wifi1s,wifi2r,wifi2s,Gsent,Grecv,runningapps,displayon,ischarging]'''
        datatopredict=[[1,2,wifi1r,wifi1s,wifi2r,wifi2s,Gsent,Gsent,runningapps,displayon,ischarging,batterylevel]]
        print(tid,tst,lat,lon,wifi1r,wifi1s,wifi2r,wifi2s,Gsent,Grecv,runningapps,displayon,batterylevel,ischarging)
        print ('LOGGED')
        datatopredict1= preprocessing.normalize(datatopredict)
        print(datatopredict1)
        pred = model.predict(datatopredict1)
        print("PPPPPPPPPPPPPPPP")
        print(pred)
                
        if pred==0:
            mess='malicious'
            
        else:
            if pred==1:
                print("not malicioius")
                mess='not malicious'
                publish.single('malicious',mess,qos=2,hostname=broker,port=broker_port,auth={'username':user,'password':passwd})
                print("reached")
                

    if messaged[0]=='t':
        print("result recieved")
        user_file=open(path, 'a+')
        user_file.write("458;112233445566;16-04-2019;10;3;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;1\n"%(wifi1r,wifi1s,wifi2r,wifi2s,Gsent,Grecv,runningapps,displayon,batterylevel,ischarging))
        user_file.close()        
        client.disconnect()
        client.loop_stop()
        return
           
mqttuser =''  
mqttpass=''
port=0
username=''
while True:
      conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='admin'")
      cur = conn.cursor()
      cur.execute('SELECT username,password,port,mqttuser,mqttpass from "people"')
      rows = cur.fetchall()
      print("done")
      print ("\nShow me the databases:\n")
      for row in rows:
          username=row[0]
          password=row[1]
          port=row[2]
          mqttuser=row[3]
          mqttpass=row[4]
          print(username,password,port,mqttuser,mqttpass)
          #print(row[0],row[1],row[2],row[3],row[4])  
        # mqttconn(row[0],row[1],row[2],row[3],row[4])
          mqttconn(username,password,port,mqttuser,mqttpass)
          print("returned")


