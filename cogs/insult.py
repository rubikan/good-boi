import discord
import random
import requests
import uuid

from util import const
from discord.ext import commands


class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_random_insult():
        url = random.choice(list(const.API_URLS))

        # Workaround because evilinsult.com caches requests in a weird way
        # https://github.com/EvilInsultGenerator/website/issues/23
        if const.EVILINSULT in url:
            url = url + "&random=" + str(uuid.uuid4())

        return requests.get(url, headers=const.REQUEST_HEADERS).text

    @commands.command()
    async def insultme(self, ctx):
        await ctx.send(f"{ctx.author.mention} {self.get_random_insult()}")
        await ctx.message.delete()

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member):
        await ctx.send(f"{member.mention} {self.get_random_insult()}")
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Insult(bot))
