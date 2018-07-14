import os
import os.path

import constants
import util

print('[{0}] Loading NLP data'.format(constants.FULL_NAME))

def __clean(path):
	"""Strip leading directories and trailing file extension from ``path``"""
	return os.path.splitext(os.path.basename(os.path.normpath(path)))[0]

words = {}
for path in [os.path.join('data/wordlists/nlp', child) for child in os.listdir('data/wordlists/nlp')] + \
			[os.path.join('data/wordlists/shared', child) for child in os.listdir('data/wordlists/shared')]:
	words[__clean(path)] = util.load_wordlist(path)
