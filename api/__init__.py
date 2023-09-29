
from .is_persons_name import IsPersonsName


ApiMethods = {
	"IsPersonsName": IsPersonsName
}


def execute(method, **kwargs):
	if method in ApiMethods:
		print(ApiMethods[method](**kwargs))
		return
	raise Exception(f"Method not found: {method}")
