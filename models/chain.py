import json
import pickle
import functools


# import local modules
import sys
from pathlib import Path
root = Path(__file__).absolute().parent
sys.path.append(str(root))

import utils.math_utils as math_utils
import utils.json_helpers as json_helpers


class Chain(object):

	def __init__(self, size=1, dedupe=True):
		if (size < 1):
			raise ValueError("Size cannot be less than 1")
		self.size = size
		self.dedupe = dedupe
		self.data = {}
	
	def _newCollection(self):
		if self.dedupe:
			return set()
		return list()

	def _add(self, previous, current):
		if self.dedupe:
			self.data[previous].add(current)
			return
		self.data[previous].append(current)

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
				self.data[current] = self._newCollection()
			if None != previous:
				self._add(previous, current)
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
		return math_utils.mean(scores)

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
		return 100 * math_utils.mean(scores)

	@classmethod
	def loadJson(cls, filename):
		with open(filename, 'r', encoding="utf-8") as fh:
			raw = fh.read()
			data = json.loads(raw, cls=json_helpers.ExtendedDecoder)
			chain = Chain(size=data["size"], dedupe=data["dedupe"])
			chain.data = data["data"]
			return chain

	def dumpJson(self, filename):
		with open(filename, 'w', encoding="utf-8") as fh:
			raw = json.dumps(
				{
					"__type__": "chain",
					"size": self.size, 
					"dedupe": self.dedupe, 
					"data": self.data
				}, 
				cls=json_helpers.ExtendedEncoder)
			fh.write(raw)

	@classmethod
	def load(cls, filename):
		with open(filename, 'rb') as fh:
			return pickle.load(fh)

	def dump(self, filename):
		with open(filename, 'wb') as fh:
			pickle.dump(self, fh)

