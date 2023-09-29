import os


# import local modules
import sys
from pathlib import Path
root = Path(__file__).absolute().parent
sys.path.append(str(root))


from models.chain import Chain

chain = None
if os.path.exists('data/chain.pickle'):
	chain = Chain.load('data/chain.pickle')
else:
	chain = Chain(size=3, dedupe=True)
	with open('data/name_corpus.txt', 'r', encoding="utf-8") as fh:
		for line in fh.readlines():
			line = line.replace('\n', '')
			chain.learn(line)

chain.dump('data/chain.pickle')
chain.dumpJson('data/chain.json')


def IsPersonsName(name, **kwargs):
	return chain.calculateScore(name)
