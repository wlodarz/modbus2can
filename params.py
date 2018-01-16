#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

class Params:
	TYPE_UINT16 = 1
	TYPE_INT16 = 2

	INPUT = 2
	HOLD = 3

	params = {
		0x100 : { 'name' : "t_hc", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x100, 'modbus_reg_type' : INPUT },
		0x102 : { 'name' : "t_dhw", 'type': TYPE_UINT16, 'value' : 47.10, 'modbus_reg_addr' : 0x102, 'modbus_reg_type' : INPUT },
		0x120 : { 'name' : "t_hc_set", 'type' : TYPE_UINT16, 'value' : 34.0, 'modbus_reg_addr' : 0x120, 'modbus_reg_type' : HOLD },
		0x122 : { 'name' : "t_dhw_setpoint1", 'type': TYPE_UINT16, 'value' : 47.00, 'modbus_reg_addr' : 0x122, 'modbus_reg_type' : HOLD },
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

	def paramRegisters(self):
		# test = { 100 : 'a', 102 : 'b' }
		# ret = []
		# for p in self.params:
		# 	ret.append(p['modbus_reg_addr'])
		# print(ret)
		return test

	def setParam(self, address, value):
		print(address)
		p = self.params.get(address)
		print(p)
		if p != None:
			p['value'] = value
		else:
			print("Param not found")
			print(address)

	def setParamByName(self, name, value):
		for e in self.params.keys():
			p = self.params.get(e)
			if p['name'] == name:
				p['value'] = value

	def getParam(self, address):
		print(address)
		p = self.params.get(address)
		print(p)
		return p['value']

