import os
import discord
import logging

from discord.ext import commands
from util import const

_log = logging.getLogger(__name__)

EXTENSIONS = [
    "cogs.explosm",
    "cogs.general",
    "cogs.image_generator",
    "cogs.insult",
    "cogs.ollama_text",
    "cogs.reddit",
    "cogs.xkcd",
]


class GoodBoiBot(commands.Bot):
    command_prefix = ["boi ", "Boi "]
    description = "A good boi for your discord server"
    intents = discord.Intents.all()

    def __init__(self):
        super().__init__(
            command_prefix=self.command_prefix,
            description=self.description,
            intents=self.intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                _log.info(f"Loading extension {extension}")
                await self.load_extension(extension)
            except Exception as e:
                _log.error(f"Failed to load extension {extension}. Reason: ", e)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="boi help"))
        announce_guild_data = os.environ["GOODBOI_ANNOUNCE_GUILDS"]
        for announce_guild in announce_guild_data.split(","):
            current_guild = announce_guild.split(":")
            guild_id = int(current_guild[0])
            guild = self.get_guild(guild_id)
            channel_id = int(current_guild[1])
            channel = guild.get_channel(channel_id)
            await channel.send(const.START_MESSAGE)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(module)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

goodboi = GoodBoiBot()
goodboi.run(os.environ["GOODBOI_DISCORD_TOKEN"])
