from util import data
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong! 🏓")

    @commands.command()
    async def help(self, ctx):
        await ctx.send(data.read_string("help.md"))

def setup(bot):
    bot.add_cog(General(bot))