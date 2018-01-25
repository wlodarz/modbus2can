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
                0x002 : { 'name' : "t_hc", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x002, 'modbus_reg_type' : INPUT, 'modbus_div' : 100.0},
                0x004 : { 'name' : "t_dhw", 'type': TYPE_UINT16, 'value' : 47.1, 'modbus_reg_addr' : 0x004, 'modbus_reg_type' : INPUT, 'modbus_div' : 100.0},
                0x006 : { 'name' : "t_r1", 'type': TYPE_UINT16, 'value' : 47.1, 'modbus_reg_addr' : 0x006, 'modbus_reg_type' : INPUT, 'modbus_div' : 100.0},
                0x008 : { 'name' : "t_outdoor_ot1", 'type': TYPE_UINT16, 'value' : 0.1, 'modbus_reg_addr' : 0x008, 'modbus_reg_type' : INPUT, 'modbus_div' : 100.0},
                0x00a : { 'name' : "posmix", 'type': TYPE_UINT16, 'value' : 0.1, 'modbus_reg_addr' : 0x00a, 'modbus_reg_type' : INPUT, 'modbus_div' : 100.0},
                0x082 : { 'name' : "t_room1_setpoint", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x082, 'modbus_reg_type' : HOLD, 'modbus_div' : 100.0, 'changed' : 0},
                0x084 : { 'name' : "t_dhw_setpoint1", 'type': TYPE_UINT16, 'value' : 47.5, 'modbus_reg_addr' : 0x084, 'modbus_reg_type' : HOLD, 'modbus_div' : 100.0, 'changed' : 0},
                0x086 : { 'name' : "mode_01", 'type': TYPE_UINT16, 'value' : 3.0, 'modbus_reg_addr' : 0x086, 'modbus_reg_type' : HOLD, 'modbus_div' : 1.0, 'changed' : 0},
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

        def holdParamNames(self):
            ret = []
            for e in self.params.keys():
                p = self.params[e]
                if p['modbus_reg_type'] == self.HOLD:
                    ret += [p['name']]
            return ret

        def paramNameByAddress(self, address):
            p = self.params.get(address)
            return p['name']

        def setValue(self, param, value):
            self.lock.acquire()
            param['value'] = value
            # if param['modbus_reg_type'] == self.HOLD:
            #     param['changed'] = 1
            self.lock.release()

        def setValueByAddress(self, address, value):
            p = self.params.get(address)
            if p != None:
                self.setValue(p, value)
            else:
                print("Param not found")
                print(address)

        def setValueByName(self, name, value):
            print('Setting parameter {0:20} to {1:.10}'.format(name, value))
            for e in self.params.keys():
                p = self.params.get(e)
                if p['name'] == name:
                    self.setValue(p, value)

        def getValueByAddress(self, address):
            self.lock.acquire()
            p = self.params.get(address)
            if p != None:
                ret = p['value']
            else:
                ret = None
            self.lock.release()
            return ret

        def getValueByName(self, name):
            print('Getting parameter {0:20}'.format(name))
            for e in self.params.keys():
                p = self.params.get(e)
                if p['name'] == name:
                    return p['value']
            return None

        def getParam(self, address):
            return self.params.get(address)

        def paramChanged(self, name):
            for e in self.params.keys():
                p = self.params.get(e)
                if p['name'] == name:
                    return p['changed']

        def setParamChanged(self, name, v):
            for e in self.params.keys():
                p = self.params.get(e)
                if p['name'] == name:
                    p['changed'] = v

