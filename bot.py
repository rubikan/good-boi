import json
import discord

from discord.ext import commands

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

description = '''A good boi for your discord server'''
intents = discord.Intents.all()
config = load_config()
client = commands.Bot(command_prefix=commands.when_mentioned, description=description, intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="!gb help | boi help"))