import os
import argparse

import config
import logger
from api import execute
from api import methods

if __name__ == "__main__":

	parser = argparse.ArgumentParser(
					prog='aiml',
					description='Utilities for AI and Machine Learning',
					epilog='methods = {0}'.format(','.join(methods))
				)

	parser.add_argument('method', type=str, help='method to invoke')
	parser.add_argument('-n', '--name', default=None, type=str, nargs='?', help='persons name to analyze')
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	logger.init(verbose=args.verbose)

	result = execute(**vars(args))
	print(result)
	exit(0)