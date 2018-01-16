#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)

import params
from multiprocessing import Queue, Process

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
		self.updater_process = Process(target=self.updater_function, args=(queue,))
		self.updater_process.start()
 
		# prepare and start CAN process
		self.hpsu_process = Process(target=self.hpsu_handler, args=(queue,))
		self.hpsu_process.start()

	def updater_function(self, queue):
		'''
		'''

		while True:
			print("updating")
			for param in self.params.paramNames():
				queue.put("g:"+param)
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
				print("can getter")
				setValue = None
				cmd = [cmd[1]]
				
			if cmd[0] == 's':
				print("can setter")	
				setValue = cmd[2]
				cmd = [cmd[1], cmd[2]]
			print(cmd)

			# print(hpsu.commands)
			for c in hpsu.commands:
				if c['name'] == cmd[0]:
					print(c)
					if setValue:
						# v = 
						# v = int(float(setValue) * float(div))
						print("Sending")
						val = cmd[1]
						div = c['div']
						v = int(float(val) * float(div))
						cmd[1] = str(v)
						setValue = cmd[1]
						print(v)
						print(cmd)
					else:
						print("Receiving")
					rc = hpsu.sendCommand(c, setValue)
					if rc != "KO":
						if not setValue:
							print("Current value")
							response = hpsu.parseCommand(cmd=c, response=rc, verbose=self.verbose)
							resp = hpsu.umConversion(cmd=c, response=response, verbose=self.verbose)
							div = c['div']
							v = int(float(resp) * float(div))
							print(div)
							print(resp)
							print(v)
							print("GET COMMAND OK")
							self.params.setValueByName(paramName, float(resp))
						else:
							print("SET COMMAND OK")
					else:
						hpsu.printd('error', 'command %s failed' % (c["name"]))

