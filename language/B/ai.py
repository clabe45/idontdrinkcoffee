import random
from datetime import datetime
from textblob import TextBlob

import nlg
import nlp

POSITIVITY_THRESHOLD = +0.2		# whether a statement is considered positive
NEGATIVITY_THRESHOLD = -0.2		# whether a statement is considered negative
SUBJECTIVITY_THRESHOLD = 0.7	# whether a statement is considered subjective
CAPS_THRESHOLD = float(2) / float(3)	# a percentage for whether a statement is considered to be in "caps"
TIME_THRESHOLD = 12 + 6		# in hours; the start of nighttime

class Agent():
	def __init__(self, bot):
		self.bot = bot

	def respond(self, message):
		text = message.content
		parsed = TextBlob(text)

		first_person = 	False	# whether the first person was mentioned using a pronoun
		second_person = False
		for word in parsed.words:
			if word.lower() in nlp.words['1st_person_sing'] + nlp.words['1st_person_plur']:
				first_person = True
			elif word.lower() in nlp.words['2nd_person']:
				second_person = True
		mentioned = self.bot.user in message.mentions
		excited = '!' in text or _is_caps(text)

		if '?' in text:	# if it's a question, then respond_statement will make no sense
			return self.respond_question(message, parsed, (first_person, second_person, mentioned, excited))

		return self.respond_statement(message, parsed, (first_person, second_person, mentioned, excited))

	def respond_statement(self, message, parsed, flags):
		first_person, second_person, mentioned, excited = flags

		for word in parsed.words:
			if word.lower() in nlp.words['greeting']:
				return nlg.choice('greeting')
			if word.lower() in nlp.words['leaving'] or word.lower() in nlp.words['bye']:
				return nlg.choice('bye.nighttime') if _is_nighttime() and random.randint(0, 1) == 0 else nlg.choice('bye')

		if parsed.sentiment.polarity >= POSITIVITY_THRESHOLD:
			if mentioned and second_person and not first_person: return nlg.choice('complimented')
			if random.randint(0, 1) == 0: return nlg.choice('compliment') + ('!' if excited else '')
			return None
		if parsed.sentiment.polarity <= NEGATIVITY_THRESHOLD:
			if mentioned and second_person: return nlg.choice('insulted')
			if excited: return nlg.choice('sooth')
			if random.randint(0, 1) == 0: 	# combined to make code simpler
				if parsed.sentiment.subjectivity > SUBJECTIVITY_THRESHOLD: return nlg.choice('subjective')
				return nlg.choice('insult')
			return None
		if random.randint(0, 2) == 0: return nlg.choice('neutral')
		return None

	def respond_question(self, message, parsed, flags):
		first_person, second_person, mentioned, excited = flags
		if not mentioned: return None

		return nlg.choice('idk')

def _is_nighttime():
	return datetime.now().hour > TIME_THRESHOLD

def _is_caps(text):
	if len(text) == 0: return False	# prevent / by 0
	return float(sum([1 for c in text if c.isupper()])) / float(len(text)) >= CAPS_THRESHOLD
