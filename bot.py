import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
from json import load

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



@bot.event
async def on_ready():
    await bot.tree.sync()
    print('------')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    activity = discord.Activity(name="becoming the best bot on IRF", type=5)
    await bot.change_presence(activity=activity)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

@app_commands.command(name="saygoodbye")
async def goodbye(interaction: discord.Interaction):
    if interaction.user.id == 267672597045575690:
        print("yes")
    else:
        await interaction.response.send_message("command not found", ephemeral=True)

asyncio.run(main())
