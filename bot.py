#bot.py
#Initial code by: https://realpython.com/how-to-make-a-discord-bot-python/
#Author: Jonah Monaghan
# 02-25-2020
import os
import discord
import random
import playerClass

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix='!')

dice = [1, 1, 1, 1, 1]
players = []


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(f'{bot.user} has connected to:\n' f'{guild.name}(id: {guild.id})')


@bot.command()
async def roll(ctx):
    rollerName = ctx.message.author.display_name
    roller = None
    for player in players:
        if player.name == rollerName:
            roller = player
            break
    if roller != None:
      if roller.GetRollCount() > 0:
        if(roller.GetChosen() == True):
            roller.MakeRoll()
            dice.clear()
            strSend = roller.name + " rolled:\n"
            for i in range(1, roller.GetRemainingDice()):
              tmpRoll = random.randrange(1, 7)
              dice.append(tmpRoll)
              roller.SetTableDice(tmpRoll)
              strSend += "#" + str(i) + ": " + str(dice[i - 1]) + "\n"
            strSend += "Which dice would you like to keep?"
        else:
          strSend = "Don't get hasty! You need to choose from your last roll!"
      else:
        strSend = "You have reached your roll limit!"
    else:
      strSend = ":x:" + rollerName + " is not a player:x:"
    await ctx.send(strSend)


@bot.command()
async def holds(ctx):
    sendStr = ""
    holderName = ctx.message.author.display_name
    holderMention = ctx.message.author.mention
    holder = None
    for player in players:
        if player.name == holderName:
            holder = player
            break
    if holder != None:
      sendStr = holderMention + " you are holding:\n"
      sendStr += str(holder.GetHoldDice())
    else:
      sendStr = ":x:" + holderName + " is not a player:x:"
    await ctx.send(sendStr)

@bot.command()
async def table(ctx):
    sendStr = ""
    holderName = ctx.message.author.display_name
    holderMention = ctx.message.author.mention
    holder = None
    for player in players:
        if player.name == holderName:
            holder = player
            break
    if holder != None:
      sendStr = holderMention + " your table has:\n"
      sendStr += str(holder.GetTableDice())
    else:
      sendStr = ":x:" + holderName + " is not a player:x:"
    await ctx.send(sendStr)

@bot.command()
async def keep(ctx, arg, die2=0, die3=0, die4=0, die5=0):
    chooserName = ctx.message.author.display_name
    chooser = None
    for player in players:
        if player.name == chooserName:
            chooser = player
            break
    try:
        arg = int(arg)
    except ValueError:
        print(f'Cannot convert to int')

    if isinstance(arg, str):
        if str(arg).lower() == "all":
            #Disable rolling, enable scoring
            for value in chooser.GetTableDice():
              chooser.SetHoldDice(value)
              chooser.SetChosen(True)
            print(f'All dice saved')
        elif str(arg).lower() == "none":
            chooser.SetChosen(True)
            print(f'No dice saved')
        else:
            await ctx.send(":x:That is not a valid parameter:x:")
    elif isinstance(arg, int):
        print(f'Its a number!')
        if (arg > 0 and arg < chooser.GetRemainingDice()):
            tmpTableDice = chooser.GetTableDice()
            chooser.SetHoldDice(tmpTableDice[arg - 1])
            print(f'Dice number ' + str(arg) + ' saved')
        else:
            await ctx.send(":x:That is not a valid parameter:x:")


@bot.command()
async def join(ctx):
    name = ctx.message.author.display_name
    isPlaying = False
    for player in players:
        if player.name == name:
            isPlaying = True
            await ctx.send(":x:This user is already playing:x:")
            break
    if isPlaying == False: 
      players.append(playerClass.Player(name))
      await ctx.send(name + " has joined the battle!")


@bot.command()
async def getplayers(ctx):
    strSend = "The current players are:\n"
    if len(players) > 0:
        for player in players:
            strSend += player.name + "\n"
    else:
        strSend = "There are no players in this game."
    await ctx.send(strSend)


bot.run(TOKEN)
