#bot.py
#Initial code by: https://realpython.com/how-to-make-a-discord-bot-python/
#Author: Jonah Monaghan
import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix='!')

dice = [1, 1, 1, 1, 1]

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
      f'{bot.user} has connected to:\n'
      f'{guild.name}(id: {guild.id})'
    )

@bot.command(name='roll')
async def roll(ctx):
  strSend = "You rolled:\n"
  dice.clear()
  for i in range(1, 6):
    dice.append(random.randrange(1, 7))
    strSend += "#" + str(i) + ": " + str(dice[i - 1]) + "\n"
  strSend += "Which dice would you like to keep?"
  await ctx.send(strSend)

@bot.command(name='dice')
async def mydice(ctx):
  strSend = str(dice)
  await ctx.send(strSend)

bot.run(TOKEN)
