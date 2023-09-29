import os
import argparse

from api import *


ApiMethods = {
	"IsPersonsName": IsPersonsName
}


def do(method, **kwargs):
	if method in ApiMethods:
		print(ApiMethods[method](**kwargs))
		return
	raise Exception(f"Method not found: {method}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
					prog='ProgramName',
					description='What the program does',
					epilog='Text at the bottom of help')

	parser.add_argument('method', type=str, help='method to invoke')
	parser.add_argument('-n', '--name', default=None, type=str, nargs='?', help='persons name to analyze')
	args = parser.parse_args()
	do(**vars(args))
