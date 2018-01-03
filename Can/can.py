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
	driver = "PYCAN"
	logger = None
	port = None
	lg_code = None

	def __init__(self, config, queue, params):
		'''
		'''
		print("CanBus init")

		self.update_interval = config.update_interval

		self.queue = queue
		self.params = params

		# prepare and start parameter updater process
		self.updater_process = Process(target=self.updater_function, args=(queue, params))
		self.updater_process.start()
 
		# prepare and start CAN process
		self.hpsu_process = Process(target=self.hpsu_handler, args=(queue, params, ))
		self.hpsu_process.start()

	def updater_function(self, queue, params):
		'''
		'''

		while True:
			print("updating")
			for param in params.paramNames():
				queue.put("g:"+param)
			time.sleep(self.update_interval)

	def hpsu_handler(self, queue, params):
		'''
		'''

		while True:

			# get command
			t = queue.get()
			cmd = t.strip().split(':')
			print(cmd)


			if cmd[0] == 'g':
				print("getter")
				setValue = None
				cmd = [cmd[1]]
				
			if cmd[0] == 's':
				print("setter")	
				setValue = cmd[2]
				cmd = [cmd[1], cmd[2]]

			hpsu = HPSU(driver=self.driver, logger=self.logger, port=self.port, cmd=cmd, lg_code=self.lg_code)
			print(hpsu.commands)
			for c in hpsu.commands:
				rc = hpsu.sendCommand(c, setValue)
				if rc != "KO":
					if not setValue:
						response = hpsu.parseCommand(cmd=c, response=rc, verbose=verbose)
						resp = hpsu.umConversion(cmd=c, response=response, verbose=verbose)
						params.setParam(c["name"], resp)
						print("COMMAND OK")
						print(c["name"])
						print(resp)
				else:
					hpsu.printd('error', 'command %s failed' % (c["name"]))

