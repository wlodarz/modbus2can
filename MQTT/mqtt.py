#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import sys
import params
import time
import threading

import paho.mqtt.client as mqtt

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

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

        self.mqtt_thread = threading.Thread(target=self.mqtt_function)
        self.mqtt_thread.start()

    def mqtt_function(self):
        '''
        '''

        while True:
            time.sleep(self.mqtt_update_interval)
            print("mqtt send")
            for e in self.params.params.keys():
                # print(e)
                p = self.params.params.get(e)
                # print(p)
                s = "altherma/" + p['name']
                v = str(p['value'])
                self.mqttc.publish(s, v)

            

