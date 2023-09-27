import json
import functools



# https://mathspp.com/blog/custom-json-encoder-and-decoder



def mean(numbers):
	return sum(numbers) / len(numbers)	




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


class ChainEncoder(ExtendedEncoder):
	def encode_set(self, obj):
		return {"set": list(obj)}

	def encode_complex(self, c):
		return {"real": c.real, "imag": c.imag}

	def encode_range(self, r):
		return {"start": r.start, "stop": r.stop, "step": r.step}


class ChainDecoder(ExtendedDecoder):
	def decode_set(self, obj):
		return set(obj["set"])

	def decode_complex(self, obj):
		return complex(obj["real"], obj["imag"])

	def decode_range(self, obj):
		return range(obj["start"], obj["stop"], obj["step"])




# class SetEncoder(json.JSONEncoder):
# 	def default(self, obj):
# 		if isinstance(obj, set):
# 			return list(obj)
# 		return json.JSONEncoder.default(self, obj)



# class SetDecoder(json.JSONDecoder):
# 	def default(self, obj):
# 		if isinstance(obj, list):
# 			return set(obj)
# 		return json.JSONDecoder.default(self, obj)



class Chain(object):

	def __init__(self, size=1):
		if (size < 1):
			raise ValueError("Size cannot be less than 1")
		self.size = size
		self.data = {}
	
	def _newCollection(self):
		return set()

	@functools.cache
	def getTokens(self, text):
		text = text.lower()
		text = '_{text}_'.format(text=text)
		#return [text[i:i+self.size] for i in range(0, len(text), 1) if i+self.size-1 < len(text)]
		return [text[i:i+self.size] for i in range(0, len(text), 3) if i+self.size-1 < len(text)]

	def learn(self, text):
		if ' ' in text:
			for word in text.split(' '):
				if 0 != len(word): 
					self.learn(word)
			return
		if self.size > len(text):
			return
		previous = None
		for current in self.getTokens(text):
			if current not in self.data:
				#self.data[current] = []
				self.data[current] = self._newCollection()
			if None != previous and current not in self.data[previous]:
				#self.data[previous].append(current)
				self.data[previous].add(current)
			previous = current

	@functools.cache
	def calculateScore(self, text):
		if None == text or 0 == len(text):
			return 0
		scores = []
		if ' ' in text:
			for word in text.split(' '):
				if 0 != len(word): 
					scores.append(self._calculateScore(word))
		else:
			scores.append(self._calculateScore(text))
		if 0 == len(scores):
			return 0
		return mean(scores)

	def _calculateScore(self, text):
		scores = []
		previous = None
		for current in self.getTokens(text):
			score = 0
			if current in self.data:
				if not previous and current in self.data:
					score = 1
				elif previous and previous in self.data:
					if current in self.data[previous]:
						score = 1
			previous = current
			scores.append(score)
		return 100 * mean(scores)		

	def load(self, filename):
		with open(filename, 'r', encoding="utf-8") as fh:
			raw = fh.read()
			self.data = json.loads(raw, cls=ChainDecoder)
		print(type(list(self.data.values())[0]))

	def dump(self, filename):
		print(type(list(self.data.values())[0]))
		with open(filename, 'w', encoding="utf-8") as fh:
			raw = json.dumps(self.data, cls=ChainEncoder)
			fh.write(raw)
