#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import params
# from multiprocessing import Queue, Process
import threading

import serial
import sys
import getopt
import time
import locale
import importlib
import logging
from HPSU.HPSU import HPSU


class Can():
    ''' A main modbus class.
    '''
    update_interval = 3
    inter_param_interval = 1
    driver = "PYCAN"
    logger = None
    port = None
    lg_code = None
    verbose = 0

    def __init__(self, config, queue, params):
        '''
        '''
        print("CanBus init")

        self.update_interval = config.update_interval
        self.inter_param_interval = config.inter_param_interval

        self.queue = queue
        self.params = params

        # prepare and start parameter updater process
        self.updater_thread = threading.Thread(target=self.updater_function)
        self.updater_thread.start()
 
        # prepare and start CAN process
        self.hpsu_thread = threading.Thread(target=self.hpsu_handler, args=(queue,))
        self.hpsu_thread.start()

    def updater_function(self):
        '''
        '''

        while True:
            print("CAN: updating")
            for name in self.params.inputParamNames():
                print('CAN: updating param ' + name)
                self.queue.put("g:"+name)
                time.sleep(self.inter_param_interval)

            for name in self.params.holdParamNames():
                print('CAN: trying HOLD param {0:10}'.format(name))
                if self.params.paramChanged(name) != 0:
                    print('CAN: param {0:20} changed'.format(name))
                    v = self.params.getValueByName(name)
                    self.queue.put("s:"+name+":"+str(v))

            for name in self.params.holdParamNames():
                print('CAN: updating param ' + name)
                self.queue.put("g:"+name)
                time.sleep(self.inter_param_interval)


            time.sleep(self.update_interval)

    def hpsu_handler(self, queue):
        '''
        '''

        hpsu = HPSU(driver=self.driver, logger=self.logger, port=self.port, cmd=[], lg_code=self.lg_code)
        while True:

            # get command
            t = queue.get()
            cmd = t.strip().split(':')
            paramName = cmd[1]
            print(cmd)

            if cmd[0] == 'g':
                # print("can getter")
                setValue = None
                cmd = [cmd[1]]
				
            if cmd[0] == 's':
                # print("can setter")	
                setValue = cmd[2]
                cmd = [cmd[1], cmd[2]]
                print('CAN SET')
                print(cmd)

            # print(hpsu.commands)
            for c in hpsu.commands:
                if c['name'] == cmd[0]:
                    # print(c)
                    if setValue:
                            # v = 
                            # v = int(float(setValue) * float(div))
                            print("Sending")
                            val = cmd[1]
                            div = c['div']
                            v = int(float(val) * float(div))
                            cmd[1] = str(v)
                            setValue = cmd[1]
                            # print(v)
                            print('CAN: sending set command {0} {1}'.format(c, setValue))
                    
                    # print("Receiving")
                    rc = hpsu.sendCommand(c, setValue)
                    if rc != "KO":
                        if not setValue:
                            # print("Current value")
                            response = hpsu.parseCommand(cmd=c, response=rc, verbose=self.verbose)
                            resp = hpsu.umConversion(cmd=c, response=response, verbose=self.verbose)
                            div = c['div']
                            v = int(float(resp) * float(div))
                            # print(div)
                            # print(resp)
                            # print(v)
                            # print("GET COMMAND OK")
                            self.params.setValueByName(paramName, float(resp))
                            print("CAN: GET COMMAND OK")
                        else:
                            self.params.setParamChanged(paramName, 0)
                            print("CAN: SET COMMAND OK")
                    else:
                        hpsu.printd('CAN: error', 'command %s failed' % (c["name"]))

