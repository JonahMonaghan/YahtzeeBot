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