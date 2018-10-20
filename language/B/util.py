import os.path

def load_wordlist(name, lower=False):
	file = open(name)
	ls = [ln.lower().strip() if lower else ln.strip() for ln in file.readlines()]
	file.close()
	return ls

def get_secret_key():
	file = open(os.path.join('data', 'key.txt'))
	key = file.read()
	file.close()
	return key
