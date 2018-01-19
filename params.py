#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import threading

class Params:
        TYPE_UINT16 = 1
        TYPE_INT16 = 2

        INPUT = 2
        HOLD = 3

        params = {
                0x100 : { 'name' : "t_hc", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x100, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x102 : { 'name' : "t_dhw", 'type': TYPE_UINT16, 'value' : 47.1, 'modbus_reg_addr' : 0x102, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x104 : { 'name' : "t_return", 'type': TYPE_UINT16, 'value' : 47.1, 'modbus_reg_addr' : 0x104, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x106 : { 'name' : "t_outdoor_ot1", 'type': TYPE_UINT16, 'value' : 0.1, 'modbus_reg_addr' : 0x106, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x108 : { 'name' : "posmix", 'type': TYPE_UINT16, 'value' : 0.1, 'modbus_reg_addr' : 0x108, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                # 0x120 : { 'name' : "t_hc_set", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x120, 'modbus_reg_type' : HOLD, 'modbus_div' : 10.0},
                # 0x122 : { 'name' : "t_dhw_setpoint1", 'type': TYPE_UINT16, 'value' : 47.5, 'modbus_reg_addr' : 0x122, 'modbus_reg_type' : HOLD, 'modbus_div' : 10.0},
                }

        def __init__(self):
            print("Init params")
            self.lock = threading.Lock()

        def paramNames(self):
            ret = []
            for e in self.params.keys():
                p = self.params[e]
                ret += [p['name']]
            return ret

        def inputParamNames(self):
            ret = []
            for e in self.params.keys():
                p = self.params[e]
                if p['modbus_reg_type'] == self.INPUT:
                    ret += [p['name']]
            return ret

        def paramName(self, address):
            p = self.params.get(address)
            return p['name']

        def setValue(self, address, value):
            p = self.params.get(address)
            if p != None:
                p['value'] = value
            else:
                print("Param not found")
                print(address)

        def setValueByName(self, name, value):
            self.lock.acquire()
            for e in self.params.keys():
                p = self.params.get(e)
                p = self.params.get(e)
                if p['name'] == name:
                    p['value'] = value
            self.lock.release()

        def getValue(self, address):
            self.lock.acquire()
            p = self.params.get(address)
            if p != None:
                ret = p['value']
            else:
                ret = None
            self.lock.release()
            return ret

        def getParam(self, address):
            return self.params.get(address)

