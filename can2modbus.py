#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v 0.0.1 by Wlodzimierz Kalawski (Wlodarz)


import sys
sys.path.append('hpsu')

from params import Params
from config import config
from multiprocessing import Queue
from ModBus.modbus import ModBus
from Can.can import Can

def main(argv):

	# prepare communication queue
	queue = Queue()

	# prepare device params list
	params = Params()

	# prepare CanBus object handler
	can = Can(config, queue, params)

	# prepare ModBus object handler
	modbus = ModBus(config, queue, params)

if __name__ == "__main__":
    main(sys.argv[1:])
