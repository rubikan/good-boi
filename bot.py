import discord
import json
import logging
import os

from discord.ext import commands

_log = logging.getLogger(__name__)

EXTENSIONS = [
    "cogs.explosm",
    "cogs.general",
    "cogs.image_generator",
    "cogs.insult",
    "cogs.reddit",
    "cogs.voice",
    "cogs.xkcd",
]


def load_config():
    with open("data/config.json", "r") as f:
        config = json.load(f)
        # the replicate API wants the API token as an environment variable
        os.environ["REPLICATE_API_TOKEN"] = config["REPLICATE_TOKEN"]
        return config


class GoodBoiBot(commands.Bot):
    command_prefix = ["boi ", "Boi "]
    description = "A good boi for your discord server"
    intents = discord.Intents.all()
    config = load_config()

    def __init__(self):
        super().__init__(
            command_prefix=self.command_prefix,
            description=self.description,
            intents=self.intents,
            help_command=None,
        )
        discord.opus.load_opus("/usr/lib/libopus.so")

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                _log.info(f"Loading extension {extension}")
                await self.load_extension(extension)
            except Exception as e:
                _log.info(f"Failed to load extension {extension}. Reason: ", e)
                print(e)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="boi help"))
        if "ANNOUNCE_GUILDS" in self.config:
            for announce_guild in self.config["ANNOUNCE_GUILDS"]:
                guildId = int(announce_guild["GUILD_ID"])
                guild = self.get_guild(guildId)
                channelId = int(announce_guild["CHANNEL_ID"])
                channel = guild.get_channel(channelId)
                await channel.send("✨ I AM BACK WITH NEW FEATURES BABY ✨")


goodboi = GoodBoiBot()
goodboi.run(goodboi.config["DISCORD_TOKEN"])
