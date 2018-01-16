#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

class Params:
        TYPE_UINT16 = 1
        TYPE_INT16 = 2

        INPUT = 2
        HOLD = 3

        params = {
                0x100 : { 'name' : "t_hc", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x100, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x102 : { 'name' : "t_dhw", 'type': TYPE_UINT16, 'value' : 47.10, 'modbus_reg_addr' : 0x102, 'modbus_reg_type' : INPUT, 'modbus_div' : 10.0},
                0x120 : { 'name' : "t_hc_set", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x120, 'modbus_reg_type' : HOLD, 'modbus_div' : 10.0},
                0x122 : { 'name' : "t_dhw_setpoint1", 'type': TYPE_UINT16, 'value' : 47.00, 'modbus_reg_addr' : 0x122, 'modbus_reg_type' : HOLD, 'modbus_div' : 10.0},
                }

        def paramNames(self):
            ret = []
            for e in self.params.keys():
                p = self.params[e]
                ret += [p['name']]
            return ret

        def paramName(self, address):
            print(address)
            p = self.params.get(address)
            print(p['name'])
            return p['name']

        def setValue(self, address, value):
            print(address)
            p = self.params.get(address)
            print(p)
            if p != None:
                p['value'] = value
            else:
                print("Param not found")
                print(address)

        def setValueByName(self, name, value):
            for e in self.params.keys():
                p = self.params.get(e)
                if p['name'] == name:
                       p['value'] = value

        def getValue(self, address):
            print(address)
            p = self.params.get(address)
            if p != None:
                print(p)
                return p['value']
            else:
                return None

        def getParam(self, address):
            return self.params.get(address)

