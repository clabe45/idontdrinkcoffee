import random
import os
import os.path

import util
import constants

# Note: nlg.words['greeting'] is distinct from nlp.words['greeting'] because it preserves case

print('[{0}] Loading NLG data'.format(constants.FULL_NAME))

def __clean(path):
	"""Strip leading directories and trailing file extension from ``path``"""
	return os.path.splitext(os.path.basename(os.path.normpath(path)))[0]

words = {}
for path in [os.path.join('data/wordlists/nlg', child) for child in os.listdir('data/wordlists/nlg')] + \
			[os.path.join('data/wordlists/shared', child) for child in os.listdir('data/wordlists/shared')]:
	words[__clean(path)] = util.load_wordlist(path)	# set last part of path to the wordlist

def choice(category, capitalize=False):
	chosen = random.choice(words[category])
	return chosen.capitalize() if capitalize else chosen
