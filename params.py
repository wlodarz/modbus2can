#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

class Params:
	TYPE_UINT16 = 1
	TYPE_INT16 = 2

	INPUT = 2
	HOLD = 3

	params = {
		0x100 : { 'name' : "t_dhw", 'type': TYPE_UINT16, 'value' : 1, 'modbus_reg_addr' : 0x100, 'modbus_reg_type' : HOLD },
		0x102 : { 'name' : "t_hs", 'type' : TYPE_UINT16, 'value' : 3, 'modbus_reg_addr' : 0x101, 'modbus_reg_type' : HOLD },
		0x104 : { 'name' : "t_hc", 'type' : TYPE_UINT16, 'value' : 5, 'modbus_reg_addr' : 0x102, 'modbus_reg_type' : HOLD },
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

	def setParam(self, name, value):
		for p in self.params:
			if p['name'] == name:
				p['value'] = value

	def getParam(self, address):
		print(address)
		p = self.params.get(address)
		print(p)
		return p['value']

