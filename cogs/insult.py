import discord
import random
import requests
import uuid

from discord.ext import commands

API_URLS = { "https://evilinsult.com/generate_insult.php?lang=en&type=text","https://insult.mattbas.org/api/insult.text" }
EVILINSULT = "evilinsult.com"

class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_random_insult():
        url = random.choice(list(API_URLS))

        # Workaround because evilinsult.com caches requests in a weird way
        # https://github.com/EvilInsultGenerator/website/issues/23
        if EVILINSULT in url:
            url = url + "&random=" + str(uuid.uuid4())

        return requests.get(url).text

    @commands.command()
    async def insultme(self, ctx):
        await ctx.send(f'{ctx.author.mention} {self.get_random_insult()}')

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member):
        await ctx.send(f'{member.mention} {self.get_random_insult()}')

def setup(bot):
    bot.add_cog(Insult(bot))