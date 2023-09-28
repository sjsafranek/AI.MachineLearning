import json


# https://mathspp.com/blog/custom-json-encoder-and-decoder


class ExtendedDecoder(json.JSONDecoder):

	def __init__(self, **kwargs):
		kwargs["object_hook"] = self.object_hook
		super().__init__(**kwargs)

	def object_hook(self, obj):
		try:
			name = obj["__extended_json_type__"]
			decoder = getattr(self, f"decode_{name}")
		except (KeyError, AttributeError):
			return obj
		else:
			return decoder(obj)

	def decode_set(self, obj):
		return set(obj["set"])

	def decode_complex(self, obj):
		return complex(obj["real"], obj["imag"])

	def decode_range(self, obj):
		return range(obj["start"], obj["stop"], obj["step"])



class ExtendedEncoder(json.JSONEncoder):
	
	def default(self, obj):
		name = type(obj).__name__
		try:
			encoder = getattr(self, f"encode_{name}")
		except AttributeError:
			super().default(obj)
		else:
			encoded = encoder(obj)
			encoded["__extended_json_type__"] = name
			return encoded

	def encode_set(self, obj):
		return {"set": list(obj)}

	def encode_complex(self, c):
		return {"real": c.real, "imag": c.imag}

	def encode_range(self, r):
		return {"start": r.start, "stop": r.stop, "step": r.step}


