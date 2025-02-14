import os

import discord
from discord.ext import commands

from keep_alive import keep_alive

usernames = []
counts = []

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("{0.user} Bot online".format(client))

@client.event
async def on_message(message):
  global usernames
  global counts

  countSave = 0
  
  first = True
  nWord = False
  word = ""
  words = []

  text = message.content

  for i in text:
    if first and i.lower() == "n":
      nWord = True
      first = False
      word = word + i
    
    elif nWord and i.isalpha():
      word = word + i
    
    else:
      nWord = False
      first = True
    
      if word != "":
        words.append(word)
        word = ""

  if word != "":
    words.append(word)
    word = ""
    if usernames.count(message.author) == 0:
      usernames.append(message.author)
      counts.append(len(words))

    else:
      countSave = counts[usernames.index(message.author)]
      counts.pop(usernames.index(message.author))
      counts.insert(usernames.index(message.author), countSave + len(words))
  #put counter code here
  #use message.author to find person's username.
  #you can put that in an array for storage
  #and an array with their count in the matching position.

bot = commands.Bot(command_prefix='/', intents = discord.Intents.all())

@bot.command()
async def count(ctx: commands.Context, message):
  nameStart = False
  name = ""
  
  for i in message.content:
    if i == " ":
      nameStart = True
    elif nameStart:
      name = name + i
  
  if usernames.count(name) == 0:
    await ctx.send(name + "has not said the n word yet")
  else:
    await ctx.send(name + "has said the n word " + str(counts[usernames.index(name)]) + " times")
#===========================================================
#bot = commands.Bot(command_prefix='/', intents = #discord.Intents.all())
#
#@bot.command()
#async def greet(ctx: commands.Context):
#  await ctx.send("Hello There!")
#===========================================================
#use this idea to snatch usernames and counts from the arrays if asked for
#maybe smth like "/count" then have the bot ask for a user name
#use on_message like earlier
#

keep_alive()

try:
  client.run(os.environ['TOKEN'])
except:
  os.system('kill 1')
  client.run(os.environ["TOKEN"])
#this just runs the code