import asyncio

import discord
from discord.ext import commands

import util
import constants
import ai

#TIMER_DELAY = 8

class CoffeeBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix='$', description='A simple simple reflex agent written in Python')
		self.__add_commands()
		# self.timer = None
		self.channel = None
		self.ai = ai.Agent(self)

	def __add_commands(self):
		for cmd in (self.info, self.sleep):
			self.add_command(cmd)

	async def on_ready(self):
		print('[{0}] Logged in'.format(constants.NAME))
		self.channel = self.get_channel(466444242860900362 if constants.TESTING else 466438128987799553)
		# await asyncio.sleep(constants.TIMER_DELAY)
		# self.timer = self.loop.create_task(self.on_timer())

	# def __last_message(self):
	# 	history = list(self.channel.history(limit=1))
	# 	return history[0] if history else None

	# async def on_timer(self):
	# 	await self.channel.send('tmr')
	# 	self.timer.cancel()
	# 	self.timer = None

	async def on_message(self, message):
		if not self.is_ready(): return
		await self.process_commands(message)
		if message.author == self.user or message.content.startswith(self.command_prefix): return

		response = self.ai.respond(message)
		if response: await self.channel.send(response)

		# if self.timer:
		# 	self.timer.cancel()
		# # only start conversation TIMER_DELAY seconds after last message is sent
		# await asyncio.sleep(constants.TIMER_DELAY)
		# self.timer = self.loop.create_task(self.on_timer())

	@commands.command()
	async def info(self, ctx):
		if ctx.channel == self.channel:
			await ctx.send('I am a Pythonic bot [{0}]. You?'.format(constants.FULL_NAME))

	@commands.command()
	@commands.has_role('manage_bots')
	async def sleep(self, ctx):
		if ctx.channel == self.channel:
			await self.close()
			print('[{0}] Logged out'.format(constants.NAME))

bot = CoffeeBot()
bot.run(util.get_secret_key())
