from functools import partial

import discord
from discord.ext import commands

# https://stackoverflow.com/a/5910893/378315
class CommandManager:
	'''Wrap Discord's |commands.command| and stores functions in a temporary registry,
	which is populated and stored per-class definition.

	Because of the temporary registry, multiple classes are supported.
	'''

	def __init__(self):
		'''Start a new session.'''
		self.all = {}

	def has_commands(self, cls):
		'''Collect functions from past session and start a new one.

		Must be called for every class that uses the |command| decorator.
		'''

		cls.commands = self.all	# static property storing all of the class's commands
		self.all = {}
		return cls

	def command(self, description, args='', name=None, aliases=[], **kwargs):
		'''Wrapper decorator for Discord's |commands.command|'''

		this = self
		def custom_dec(func, name, **kwargs):
			if name is None: name = func.__name__
			usage = name + ' ' + args
			decorator = commands.command(aliases=aliases, name=name, **kwargs)
			R = decorator(func)		# call decorator
			# only store an object storing command metadata, don't store discord Command instance,
			# because that needs to be accessed from the bot (with __get__ and instance)
			this.all[func.__name__] = CommandMeta(name, description, usage, aliases)
			return R

		return partial(custom_dec, name=name, **kwargs)

# inherit from Discord's @commands.command
# use unbound class function of the target decorator
CommandManager.command.__name__ = commands.command.__name__
CommandManager.command.__doc__ = commands.command.__doc__

class CommandMeta:
	def __init__(self, name, description, usage, aliases):
		self.name = name
		self.description = description
		self.usage = usage
		self.aliases = aliases

	def __str__(self):
		return """```
{0}:
	Usage: {1}
	Aliases: {2}
	Description: {3}
```""".format(self.name, self.usage, ', '.join(self.aliases) if self.aliases else '/', self.description)
