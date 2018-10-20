import random
import asyncio

import util
import command
import constants

from mpmath import mp
import sympy
from sympy.parsing import sympy_parser
import discord
from discord.ext import commands

# configure mpmath
mp.dps = constants.DEFAULT_PRECISION

cm = command.CommandManager()

@cm.has_commands
class CoffeeBot(commands.Bot):
	'''The math bot'''

	def __init__(self):
		super().__init__(command_prefix='$', description='A math bot written in Python')
		self.__config_commands()
		self.channel = None
		self.testing = util.read_testing()
		self.xp = util.read_xp()

	def __config_commands(self):
		self.remove_command('help')	# remove default help command
		for name in CoffeeBot.commands:
			self.add_command(getattr(self, name))	# add function (first element in tuple)

	async def on_ready(self):
		print('[{0}] Logged in'.format(constants.NAME))
		await self.update_channel()

	async def on_message(self, message):
		if message.author == self.user: return

		is_command = message.content.startswith(self.command_prefix)
		if is_command and message.channel != self.channel:
			# invalid place to query command
			await message.author.send(
				("I heard my name. You think I can be in every channel at once? " +\
				"lol, I can't. I'm in <#{0}> rn.").format(self.channel.id)
				)
			return

		# if first word is '$'
		if ' ' in message.content and message.content[:message.content.index(' ')] == '$':
			s = message.content[len(self.command_prefix + ' '):]	# cut off prefixing '$ '
			await self.math(s)
		else:
			await self.process_commands(message)

		if is_command: return
		# do more stuff, if necessary

	async def on_command_error(self, ctx, error):
		await self.show_error(error)

	async def math(self, expr):
		try:
			await self.channel.send(str(sympy_parser.parse_expr(expr)))
		except (SyntaxError, TypeError) as e:	# TODO: probably add more
			await self.show_error(e)

	@cm.command(description='`"""Display information about |self|"""`')
	async def info(self, ctx):
		await ctx.send('I am __{0}__'.format(constants.FULL_NAME))
		# execute self.say_hello() about a second later

	@cm.command(description='Lists all commands, or displays information of a specific command',
		args='[command]')
	async def help(self, ctx, command:str = None):
		# CoffeeBot.commands is a static property
		if command is None:
			# https://stackoverflow.com/a/26672589/3783155
			await ctx.send('```\n' + '\n'.join([
				self.command_prefix + c.name + ' - ' + c.description for c in [CoffeeBot.base_command] + [
					CoffeeBot.commands[key] for key in sorted(CoffeeBot.commands.keys())
					]
				]) + '```')
		else:
			await ctx.send(CoffeeBot.commands[command])	# send CommandMeta.__str__(self)

	@cm.command(description='Prints my experience')
	async def xp(self, ctx):
		await ctx.send('My xp=' + str(self.xp))

	@cm.command(description='Stops me temporarily', aliases=['sl'])
	@commands.has_role(constants.ADMIN_ROLE)
	async def sleep(self, ctx):
		util.write_testing(self.testing)
		util.write_xp(self.xp + 1)	# increment each time the bot is run
		await self.close()

	@cm.command(description='Switches to or from test server', aliases=['mv', 'switch', 'sw'])
	@commands.has_role(constants.ADMIN_ROLE)
	async def move(self, ctx):
		'''Switch from or to the test server'''

		self.testing = not self.testing
		await self.update_channel()

	@cm.command(description='Sets the number of digits to show', args='[digits]', aliases=['precision'])
	async def prec(self, ctx, digits:int = constants.DEFAULT_PRECISION):
		'''Modify the precision of mp'''

		mp.dps = digits
		await ctx.send('Precision %s to %s' % (
			'reset' if digits==constants.DEFAULT_PRECISION else 'changed',
			digits))	# TODO: be consistent with formatting

	@cm.command(description='Prints *PI*')
	async def pi(self, ctx, digits:int = None):
		'''Send pi to the current channel'''

		if digits is None: digits = mp.dps
		dps, mp.dps = mp.dps, digits
		await ctx.send(+mp.pi)
		mp.dps = dps

	@cm.command(description='Prints *e*')
	async def e(self, ctx, digits:int = None):
		'''Send e to the current channel'''

		if digits is None: digits = mp.dps
		dps, mp.dps = mp.dps, digits
		await ctx.send(+mp.e)
		mp.dps = dps

	# :]
	@cm.command(name='count-to-ten', description='Counts from 1..10')
	async def count_to_ten(self, ctx):
		'''Counts all integers in the interval [1, 10]'''

		await ctx.send(' '.join([str(x) for x in range(1, 10+1)]))

	async def update_channel(self):
		self.channel = self.get_channel(
			constants.TEST_CHANNEL if self.testing else constants.PRODUCTION_CHANNEL
			)
		await self.say_hello()	# do I need `await`?

	async def show_error(self, e):
		embed = discord.Embed(color=discord.Color.red())
		embed.description = str(e)
		await self.channel.send(embed=embed)

	async def say_hello(self):
		'''Send a friendly message to the current channel'''

		msg = None
		t = random.randint(0, 1)	# type of message
		if 0 <= t < 1: msg = random.choice([+mp.pi, +mp.e, mp.sqrt(2)])
		elif 1 <= t < 2: msg = constants.FAVORITE_NUMBER

		await self.channel.send(msg)

CoffeeBot.base_command = command.CommandMeta('', 'Performs math', '<expr>', [])

bot = CoffeeBot()
bot.run(util.get_secret_key())
