#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import sys
import params
import time
import threading
import re

import paho.mqtt.client as mqtt

# import logging

# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

class MqttSender():
    ''' A main mqtt sender class.
    '''

    update_interval = 1

    def __init__(self, config, params):
        '''
        '''
        print("MQTT init")

        self.mqtt_update_interval = config.mqtt_update_interval

        self.params = params

        self.mqttc = mqtt.Client()
        self.mqttc.connect('localhost', 1883)
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.subscribe('altherma/set/#', qos=1)
        self.mqttc.loop_start()

        self.mqtt_thread = threading.Thread(target=self.mqtt_function)
        self.mqtt_thread.start()

    def mqtt_function(self):
        '''
        '''

        while True:
            time.sleep(self.mqtt_update_interval)
            for e in self.params.params.keys():
                p = self.params.params.get(e)
                s = "altherma/get/" + p['name']
                v = str(p['value'])
                self.mqttc.publish(s, v)
                # print(s)
            print("mqtt sent!")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))
            
    def on_message(self, client, userdata, msg):
        submsg = msg.topic.split('/')
        v = str(msg.payload, 'utf-8')
        param_name = submsg[2]
        # cmd = 's' + ':' +  submsg[2] + ':' + v
        # print(cmd)
        self.params.setValueByName(param_name, v)
        self.params.setParamChanged(param_name, 1)
        # self.queue.put(cmd)

