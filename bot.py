#bot.py
#Initial code by: https://realpython.com/how-to-make-a-discord-bot-python/
#Author: Jonah Monaghan
# 02-25-2020
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
    print(f'{bot.user} has connected to:\n' f'{guild.name}(id: {guild.id})')


@bot.command()
async def roll(ctx):
    strSend = "You rolled:\n"
    dice.clear()
    for i in range(1, 6):
        dice.append(random.randrange(1, 7))
        strSend += "#" + str(i) + ": " + str(dice[i - 1]) + "\n"
    strSend += "Which dice would you like to keep?"
    await ctx.send(strSend)


@bot.command()
async def mydice(ctx):
    strSend = str(dice)
    await ctx.send(strSend)


@bot.command()
async def keep(ctx, arg, die2=0, die3=0, die4=0, die5=0):
    
    try:
      arg = int(arg)
    except ValueError:
      print(f'Cannot convert to int')
    
    if isinstance(arg, str):
        if str(arg).lower() == "all":
            #Disable rolling, enable scoring
            print(f'All dice saved')
        elif str(arg).lower() == "none":
            print(f'No dice saved')
        else:
            await ctx.send(":x:That is not a valid parameter:x:")
    elif isinstance(arg, int):
        print(f'Its a number!')
        if (arg > 0 and arg < 7):
            #Change the roll range
            print(f'Dice number ' + str(arg) + ' saved')
        else:
            await ctx.send(":x:That is not a valid parameter:x:")


bot.run(TOKEN)
