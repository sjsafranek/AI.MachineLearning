import logging

from .is_persons_name import IsPersonsName


ApiMethods = {
	"IsPersonsName": IsPersonsName
}

methods = list(ApiMethods.keys())

def execute(method, **kwargs):
	if method in ApiMethods:
		logging.debug("execute {0}".format(method))
		return ApiMethods[method](**kwargs)
	raise Exception(f"Method not found: {method}")
