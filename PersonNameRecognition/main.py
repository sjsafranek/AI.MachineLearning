import os

from chain import Chain




# if os.path.exists('data/chain.json'):
# 	chain.load('data/chain.json')
# else:
# 	with open('data/name_corpus.txt', 'r', encoding="utf-8") as fh:
# 		for line in fh.readlines():
# 			line = line.replace('\n', '')
# 			chain.learn(line)
# 	chain.dump('data/chain.json')
# chain.dump('data/chain.json')


chain = None
if os.path.exists('data/chain.pickle'):
	chain = Chain.load('data/chain.pickle')
else:
	chain = Chain(size=3)
	with open('data/name_corpus.txt', 'r', encoding="utf-8") as fh:
		for line in fh.readlines():
			line = line.replace('\n', '')
			chain.learn(line)

chain.dump('data/chain.pickle')
chain.dumpJson('data/chain.json')


score = chain.calculateScore("stefan safranek")
print(score)

score = chain.calculateScore("lee safranek")
print(score)

score = chain.calculateScore("leennvvm")
print(score)

score = chain.calculateScore("leennvvm")
print(score)