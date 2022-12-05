from util import data, discord_utils

from discord.ext import commands
from zalgo_text import zalgo


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, argument=None):
        if argument == None:
            await ctx.send(data.read_string("help_general_1.md"))
            await ctx.send(data.read_string("help_general_2.md"))
        elif argument.lower() == "text":
            await ctx.send(data.read_string("help_general_1.md"))
            await ctx.send(data.read_string("help_general_2.md"))
        elif argument.lower() == "voice":
            await ctx.send(data.read_string("help_voice.md"))

        await ctx.message.delete()

    @commands.command()
    async def mock(self, ctx, *, arg):
        mocked = ""
        for idx in range(len(arg)):
            if not idx % 2:
                mocked = mocked + arg[idx].lower()
            else:
                mocked = mocked + arg[idx].upper()
        await ctx.send(mocked)
        await ctx.message.delete()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong! 🏓")

    @commands.command()
    async def say(self, ctx):
        argumentMessage = discord_utils.extract_clean_message(ctx)
        if ctx.message.reference is not None:
            referencedMessage = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            await referencedMessage.reply(argumentMessage)
        else:
            await ctx.send(argumentMessage)
        await ctx.message.delete()

    @commands.command()
    async def zalgo(self, ctx):
        zalgoMessage = zalgo.zalgo().zalgofy(discord_utils.extract_clean_message(ctx))
        if ctx.message.reference is not None:
            referencedMessage = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            await referencedMessage.reply(zalgoMessage)
        else:
            await ctx.send(zalgoMessage)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(General(bot))
