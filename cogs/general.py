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
        argumentMessage = discord_utils.extract_clean_message(ctx)
        if ctx.message.reference is not None:
            referencedMessage = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await referencedMessage.reply(argumentMessage)
        else:
            await ctx.send(argumentMessage)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(General(bot))