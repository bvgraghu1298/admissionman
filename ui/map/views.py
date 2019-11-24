from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import numpy as numpy
from sklearn import svm, metrics
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import preprocessing
from django.template import Context
import csv
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import ast
import pandas as pd
from sklearn import svm, metrics, preprocessing
# load data
messages="........"
def on_message(client, userdata, message):
    print("entered")
    global messages
    messaged = message.payload.decode('utf-8')
    messages= messaged
    client.disconnect()
    client.on_disconnect = on_disconnect
# Create your views here.

def index(request):
    return render(request, 'index.html', {})
def on_disconnect(client, userdata,rc=0):
    print("disconnect")
    client.loop_stop()
def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribe")


def data(request):
    print("script running")
    mqtt_client = mqtt.Client()

    # create file to store tracking points
    global messages
    # Here goes your broker IP/Address and port, username, and password if appliable
    broker = 'm16.cloudmqtt.com'
    broker_port = 17679
    user = 'mtpelhgh'
    passwd = 'pxF6nKV4sShm'
    # Connection
    mqtt_client.username_pw_set(user, passwd)
    connect= mqtt_client.connect(broker, broker_port)
    if(connect!=0):
        mqtt_client.disconnect()
        mqtt_client.connect(broker, broker_port)
    # The topic for the data will be TRACK but use what you want; must match the DEVICE script topic
    mqtt_client.subscribe('malicious', qos=2)
    mqtt_client.on_subscribe=on_subscribe
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()

    return HttpResponse(messages)



