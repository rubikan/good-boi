import os
import discord
import logging

from random import randrange
from discord.ext import commands

_log = logging.getLogger(__name__)


class AutoAnswer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowedIds = os.environ["GOODBOI_AUTOANSWER_CHANNELS"].split(",")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.allowedIds and str(message.channel.id) not in self.allowedIds:
            await self.bot.process_commands(message)
            return

        text = message.content.lower()

        if "wurst" in text or "wurscht" in text:
            await message.reply("🌭 Wurscht is a gfüllte Haut 🌭")

        if message.author.id == 323815636583317514 and 50 == randrange(100):
            await message.reply("👻 Wann spielst du endlich Phasmophobia? 👻")

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(AutoAnswer(bot))
