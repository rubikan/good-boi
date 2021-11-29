from util import data, discord_utils
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

    @commands.command()
    async def say(self, ctx):
        message = discord_utils.extract_clean_message(ctx)
        await ctx.message.delete()
        await ctx.send(message)

def setup(bot):
    bot.add_cog(General(bot))