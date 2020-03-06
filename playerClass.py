#playerClass.py
#A class that turns a discord user into the player of a Yahtzee
#Author: Jonah Monaghan
#02-25-2020

class Player:

  def __init__(self, username):
    self.name = username #The player's name
    self.rollCounter = 3 #Available rolls
    self.dice = [] #A list for the player's held dice
    self.tableDice = [] #A list for the player's table dice
    self.remainingDice = 6 #Range is EXCLUSIVE so there are only 5 dice
    self.chosen = True #If the player has chosen since their last roll
  


#Dice Functions
  def SetHoldDice(self, value): #A function that adds the value of the chosen die
    self.dice.append(value)
    self.remainingDice = self.remainingDice - 1

  def GetHoldDice(self):
    return self.dice

  def SetTableDice(self, value):
    self.tableDice.append(value)

  def ClearTableDice(self):
    self.tableDice.clear()
  
  def GetTableDice(self):
    return self.tableDice
  
  def GetRemainingDice(self):
    return self.remainingDice
  
  def SetChosen(self, tf):
    self.chosen = tf
  
  def GetChosen(self):
    return self.chosen

#Roll Counter Functions 
  def MakeRoll(self):
    self.rollCounter = self.rollCounter - 1
    self.SetChosen(False)
  
  def GetRollCount(self):
    return int(self.rollCounter)

  def ResetRolls(self):
    self.rollCounter = 3
    self.dice.clear()

#Scoring Functions

#Scoring Chart
#Ones: Add all of the ones together (Score: 1 - 5 [val * qnty])
#Twos: Add all of the twos together (Score: 2 - 10 [val * qnty])
#Threes: Add all of the threes together (Score: 3 - 15 [val * qnty])
#Fours: Add all of the fours together (Score: 4 - 20 [val * qnty])
#Fives: Add all of the fives together (Score: 5 - 25 [val * qnty])
#Sixes: Add all of the sixes together (Score 6 - 30 [val * qnty])
#Three of a Kind: Add the value of all dice as long as three are matching (Score: 5 - 36 [valAllDice])
#Four of a Kind: Add the value of all dice as long as four are matching (Score: 5 - 36 [valAllDice])
#Full House: If three of kind and pair (Score: 25 [CONST])
#Small Straight: If four dice have consecutive values (Score: 30 [CONST])
#Large Straight: If all five dice have consecutive values (Score: 40 [CONST])
#Yahtzee!: If all five dice are the same value (Score: 50 or 100 [CONST])
#Chance: No conditions (5 - 36 [valAllDice])
#Upper bonus: If Ones - Sixes score more than 63 players receive a bonus (Score: 35 [CONST])

#Rules
#Player rolls dice up to 3 times
#After player has chosen all dice or runs out rolls scoring will begin
#Player use their available dice to choose what section they will fill out (Sections can only be filled out once [Except Yahtzee])
#If no section can be filled out players must scratch a section out so that it may not be used
#If a player gets a Yahtzee (5 identical dice), they will receive 50 points.
#After the first Yahtzee, if players get any additional Yahtzees they will receive 100 points rather than the traditional 50
#Once scoring is done the players will roll again starting the cycle over again
#Once players cannot fill in any sections they will wait till the game is done
#Once all players cannot fill in any sections the game will be over
