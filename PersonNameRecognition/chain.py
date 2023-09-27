import json
import functools


class Chain(object):

	def __init__(self, size=1):
		if (size < 1):
			raise ValueError("Size cannot be less than 1")
		self.size = size
		self.data = {}
	
	@functools.cache
	def getTokens(self, text):
		text = text.lower()
		text = '_' + text + '_'
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
				self.data[current] = []
			if None != previous and current not in self.data[previous]:
				self.data[previous].append(current)
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
		return sum(scores) / len(scores)

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
		return 100 * (sum(scores) / len(scores))		

	def load(self, filename):
		with open(filename, 'r', encoding="utf-8") as fh:
			data = json.loads(fh.read())
			self.data = data

	def dump(self, filename):
		with open(filename, 'w', encoding="utf-8") as fh:
			fh.write(json.dumps(self.data))

