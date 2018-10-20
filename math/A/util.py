import os.path

# TODO: use one more complex data file
# TODO: doc more functions

def read_data(relpath, default=None):
	path = os.path.join('data', relpath)
	if not os.path.exists(path):
		with open(path, 'w') as file:
			if default is not None: file.write(default)
			print('Created %s' % path)
			file.close()
	file = open(path, 'r')	# create if doesn't exist
	file.seek(0)
	s = file.read().strip()
	file.close()
	return s

def write_data(relpath, s):
	path = os.path.join('data', relpath)
	file = open(path, 'w')
	file.write(s)
	file.close()

# TODO: stop rewriting code per bot type
def get_secret_key():
	return read_data('key.txt')

def read_testing():
	'''Whether or not the bot was in testing mode when it ended its last session.'''

	s = read_data('testing.txt', 'true')
	if s.lower() == 'true': return True
	if s.lower() == 'false': return False
	print('Error: invalid boolean in %s' % os.path.join('data', 'testing.txt'))
	return None

def write_testing(testing):
	write_data('testing.txt', str(testing).lower())

def read_xp():
	try:
		return int(read_data('xp.txt', '0'))
	except ValueError:
		print('Error: invalid integer in %s' % os.path.join('data', 'xp.txt'))

def write_xp(xp):
	write_data('xp.txt', str(xp))
