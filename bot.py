import discord
import logging

from discord.ext import commands
from util import const
from util.config import load_config

_log = logging.getLogger(__name__)

EXTENSIONS = [
    "cogs.explosm",
    "cogs.general",
    "cogs.image_generator",
    "cogs.insult",
    "cogs.reddit",
    "cogs.xkcd",
    "cogs.ai",
]


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

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                _log.info(f"Loading extension {extension}")
                await self.load_extension(extension)
            except Exception as e:
                _log.error(f"Failed to load extension {extension}. Reason: ", e)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="boi help"))
        for announce_guild in self.config.discord.announce_guilds:
            guildId = int(announce_guild.guild_id)
            guild = self.get_guild(guildId)
            channelId = int(announce_guild.channel_id)
            channel = guild.get_channel(channelId)
            await channel.send(const.START_MESSAGE)


logging.basicConfig(level=logging.INFO)
goodboi = GoodBoiBot()
goodboi.run(goodboi.config.discord.token)
