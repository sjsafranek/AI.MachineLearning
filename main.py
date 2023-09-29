import os
import argparse

from api import execute


if __name__ == "__main__":

	parser = argparse.ArgumentParser(
					prog='ProgramName',
					description='What the program does',
					epilog='Text at the bottom of help')

	parser.add_argument('method', type=str, help='method to invoke')
	parser.add_argument('-n', '--name', default=None, type=str, nargs='?', help='persons name to analyze')
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	execute(**vars(args))
