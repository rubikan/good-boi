import json

import discord

from discord.ext import commands

EXTENSIONS = [
    "cogs.general",
    "cogs.reddit"
]

def load_config():
    with open("data/config.json", "r") as f:
        return json.load(f)

class GoodBoiBot(commands.Bot):
    command_prefix = ["boi ","Boi "]
    description = "A good boi for your discord server"
    intents = discord.Intents.all()
    config = load_config()

    def __init__(self):
        super().__init__(command_prefix=self.command_prefix, description=self.description, intents=self.intents, help_command = None)
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}. Reason: ", e)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="boi help"))
    
    def run(self):
        super().run(self.config["DISCORD_TOKEN"], reconnect=True)

if __name__ == "__main__":
    goodboi = GoodBoiBot()
    goodboi.run()