#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import sys
import params
# from multiprocessing import Queue, Process
import time
import threading

from pymodbus.server.async import StartSerialServer
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSparseDataBlock, ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# class CallbackDataBlock(ModbusSparseDataBlock):
class CallbackDataBlock(ModbusSequentialDataBlock):
    def __init__(self, params, queue):
        print("init")
        self.params = params
        self.queue = queue
        super(CallbackDataBlock, self).__init__(0x00, [0]*0x3ff)

    def setValues(self, address, value):
        # print("setValues")
        # print(address)
        # print(value)
        p = self.params.getParam(address)
        v = 256*value[0] + value[1]
        vv = float(v) / p['modbus_div']
        cmd = self.params.paramName(address)
        s = 's:'+cmd+':'+str(vv)
        self.queue.put(s)
        # # super(CallbackDataBlock, self).setValues(address, value)
        # # self.queue.put((self.devices.get(address, None), value))

    def getValues(self, address, count=1):
        v = self.params.getValue(address)
        print('getValues {0:8} = {1:.1f}'.format(address, v))
        p = self.params.getParam(address)
        vv = int(float(v) * p['modbus_div'])
        high = (vv & 0xff00 ) >> 8
        low = vv & 0x00ff
        return [high, low]

class ModBus():
    ''' A main modbus class.
    '''

    update_interval = 1

    def __init__(self, config, queue, params):
        '''
        '''
        print("ModBus init")

        self.update_interval = config.update_interval

        self.queue = queue
        self.params = params

        block   = CallbackDataBlock(params, queue)
        store   = ModbusSlaveContext(di=block, co=block, hr=block, ir=block, zero_mode=True)
        slave = {
                0x02: store,
            }
        context = ModbusServerContext(slaves=store, single=True)


        identity = ModbusDeviceIdentification()
        identity.VendorName  = 'WK'
        identity.ProductCode = 'XX'
        identity.VendorUrl   = 'http://xxx.xxx'
        identity.ProductName = 'ModBus Server'
        identity.ModelName   = 'ModBus Server'
        identity.MajorMinorRevision = '1.0'

        # prepare and start ModBus process
        self.test_thread = threading.Thread(target=self.setter_function, args=(queue, ))
        self.test_thread.start()

        time = 2 # 5 seconds delay
        # StartSerialServer(context, identity=identity, port='/dev/ttyUSB0', stopbits=1, bytesize=8, parity='N', baudrate=9600, framer=ModbusRtuFramer)
        StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))


    def setter_function(self, queue):
        '''
        '''

        while True:
           print("modbus test setter")
           #self.queue.put("s:t_dhw_setpoint1:49.00")
           # print(self.params.params)
           time.sleep(self.update_interval)

