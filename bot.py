import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
from json import load
from random import shuffle
from time import sleep

config = load(open('config.json'))

'''
# i hate google part
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# i stop hating google part
'''
bot = commands.Bot(command_prefix = '$', help_command = None, intents=discord.Intents.all())

def scramble(original):
    destination = original
    shuffle(destination)
    return destination

communityStatus = [{"type": discord.ActivityType.watching, "status": "people use /ct check"}, {"type": discord.ActivityType.watching, "status": "Jon"},
                   {"type": discord.ActivityType.listening, "status": "your suggestions!"}, {"type": discord.ActivityType.competing, "status": "becoming the best bot on IRF"},
                   {"type": discord.ActivityType.watching, "status": "the Officer basement"}, {"type": discord.ActivityType.competing, "status": "testing citizens"},
                   {"type": discord.ActivityType.streaming, "status": "the candidates"}, {"type": discord.ActivityType.playing, "status": "on Sevas to recruit people"},
                   {"type": discord.ActivityType.watching, "status": "the Officer basement"}]

randomStatus = scramble(communityStatus)
currentPositionInList = 0
elementsInRandomStatus = len(randomStatus)-1

@bot.event
async def on_ready():
    await change_status.start()
    await bot.tree.sync()
    print('------')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@tasks.loop(seconds=10)
async def change_status():
    if currentPositionInList != elementsInRandomStatus:
        await bot.change_presence(activity=discord.Activity(name=randomStatus[currentPositionInList]['status'], type=randomStatus[currentPositionInList]['type']))
        currentPositionInList = currentPositionInList +1
    else:
        await bot.change_presence(activity=discord.Activity(name=randomStatus[currentPositionInList]['status'], type=randomStatus[currentPositionInList]['type']))
        currentPositionInList = 0

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

asyncio.run(main())
