#bot.py
#Initial code by: https://realpython.com/how-to-make-a-discord-bot-python/
#Author: Jonah Monaghan
#2020-02-26

#Imports
import os
import discord
import random
import playerClass


#Import froms
from discord.ext import commands
from dotenv import load_dotenv

#.env file
load_dotenv() #Load in the .env file
TOKEN = os.getenv('TOKEN') #Get the token from .env file
GUILD = os.getenv('GUILD') #Get the connected guild

bot = commands.Bot(command_prefix='!') #Set the bots command prefix to !

dice = [1, 1, 1, 1, 1] #Create list of dice
players = [] #Create list of players

#Once the bot has connected to the server provide feeback
@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(f'{bot.user} has connected to:\n' f'{guild.name}(id: {guild.id})')

#When the player rolls
@bot.command()
async def roll(ctx):
    """A command that rolls the available dice for the player. Cannot be used again until the !keep command is used. For every turn, players have a maximum of three rolls. Takes no parameters.
    
    Example: 
    !roll
    """
    #Get the name of the author to compare to players
    rollerName = ctx.message.author.display_name
    rollerMention = ctx.message.author.mention
    roller = None
    
    #Compare author name to player list
    for player in players:
        if player.name == rollerName: #If author and player names match
            roller = player #Author is the current roller
            break
    
    #If there is a roller in the player list
    if roller != None:

      if roller.GetRollCount() > 0: #If the player has rolls available
        
        if(roller.GetChosen() == True): #If the player has chosen since last roll
            roller.MakeRoll()
            dice.clear()
            strSend = roller.name + " rolled:\n"
            
            for i in range(1, roller.GetRemainingDice()): #Roll only the table dice
              tmpRoll = random.randrange(1, 7)
              dice.append(tmpRoll)
              roller.SetTableDice(tmpRoll) #Add the roll to player's table dice
              strSend += "#" + str(i) + ": " + str(dice[i - 1]) + "\n"
            
            strSend += rollerMention + " which dice would you like to keep?"
        
        else: #If the player hasn't chosen since their last 
          strSend = "Don't get hasty! You need to choose from your last roll!"
      else: #If the player has made more than 3 rolls
        strSend = "You have reached your roll limit!"
    else: #If the author isn't a player
      strSend = ":x:" + rollerName + " is not a player:x:"
    await ctx.send(strSend)


@bot.command()
async def holds(ctx):
    """Gets the player's current held dice, these are the dice that the player used the !keep command on. Takes no parameters.
     
    Example: 
    !holds
    """

    #Get the name of the author and compare it to players
    holderName = ctx.message.author.display_name
    holderMention = ctx.message.author.mention
    holder = None
    
    #Compare author name to player list
    for player in players:
        if player.name == holderName:
            holder = player
            break
    
    #If there is a holder in the player list
    if holder != None:
      sendStr = holderMention + " you are holding:\n"
      sendStr += str(holder.GetHoldDice())
    
    else: #If the author is not a player
      sendStr = ":x:" + holderName + " is not a player:x:"
    await ctx.send(sendStr)

@bot.command()
async def table(ctx):
    """Gets the player's table dice, these are the dice that are available for the player to !keep after they've used the !roll command. Takes no parameters. 
    
    Example:
    !table
    """
    #Get the name of the author and compare it to players
    holderName = ctx.message.author.display_name
    holderMention = ctx.message.author.mention
    holder = None
    
    #Compare author name to player list
    for player in players:
        if player.name == holderName:
            holder = player
            break
    
    #If there is a holder in the player list
    if holder != None:
      if(holder.GetTableDice()):
        sendStr = holderMention + " your table has:\n"
        sendStr += str(holder.GetTableDice())
      else:
        sendStr = holderMention + " you do not have any dice on the table! Try !roll."
    else:
      sendStr = ":x:" + holderName + " is not a player:x:"
    await ctx.send(sendStr)

@bot.command()
async def keep(ctx, arg, die2=0, die3=0, die4=0, die5=0):
    """Lets the player uses to choose which of the table dice they'll keep after a !roll command. Takes multiple parameters: parameter 1 <Mandatory>: (dieIndex, "all", "none")||parameters 2-5 [Optional]: (dieIndex).

    Examples:
    !keep all
    !keep none
    !keep 1 2
    !keep 3 5 2
    etc.
    """
    
    chooserName = ctx.message.author.display_name
    chooserMention = ctx.message.author.mention
    chooser = None
    for player in players:
        if player.name == chooserName:
            chooser = player
            break
    try:
        arg = int(arg)
    except ValueError:
        print(f'Cannot convert to int')
    
    sendStr = chooserMention

    if isinstance(arg, str):
        if str(arg).lower() == "all":
            #Disable rolling, enable scoring
            for value in chooser.GetTableDice():
              chooser.SetHoldDice(value)
              chooser.SetChosen(True)
            sendStr += " all dice have been saved. You are now done rolling for this turn."
            chooser.ClearTableDice()
        elif str(arg).lower() == "none":
            chooser.SetChosen(True)
            sendStr += " none of the dice have been saved. Nothing good eh?"
            chooser.ClearTableDice()
        else:
            sendStr = ":x:That is not a valid parameter:x:"
    elif isinstance(arg, int):
        print(f'Its a number!')
        if (arg > 0 and arg < chooser.GetRemainingDice()):
            tmpTableDice = chooser.GetTableDice()
            chooser.SetHoldDice(tmpTableDice[arg - 1])
            sendStr += " dice number " + str(arg) + " saved."
            chooser.ClearTableDice()
        else:
            sendStr = ":x:That is not a valid parameter:x:"
    
    await ctx.send(sendStr)


@bot.command()
async def join(ctx):
    """Joins the user to the game. Users cannot join the game more than once. Takes no parameters.

    Example:
    !join
    """
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
    """Prints the names of all the players in the game. Takes no parameters.

    Example:
    !getplayers
    """
    strSend = "The current players are:\n"
    if len(players) > 0:
        for player in players:
            strSend += player.name + "\n"
    else:
        strSend = "There are no players in this game."
    await ctx.send(strSend)


bot.run(TOKEN)
