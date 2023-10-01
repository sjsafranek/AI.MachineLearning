#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


def init(verbose=False):

	level = logging.WARNING
	if verbose:
		level = logging.DEBUG

	logging.basicConfig(
		level=level,
		datefmt='%Y-%m-%dT%H:%M:%S',
		#datefmt='%Y-%m-%dT%H:%M:%S%z',
		format="%(asctime)s [%(levelname)s] [%(threadName)s] %(filename)s %(funcName)s:%(lineno)d %(message)s"
	)
