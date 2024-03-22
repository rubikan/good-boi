from typing import Optional
from util import data, discord_utils
from discord.ext.commands import Context

from discord.ext import commands
from zalgo_text import zalgo


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: Context):
        help_message = ""
        for cog_name, cog in self.bot.cogs.items():
            help_message += f"**{cog_name}:**\n"
            for command in cog.get_commands():
                names = ", ".join([command.name, *command.aliases])

                if command.help:
                    help_message += f"**{names}** - {command.help}\n"
            help_message += "\n"
        await ctx.send(help_message)

    @commands.command(help="Mock the given text")
    async def mock(self, ctx, *, arg):
        mocked = ""
        for idx in range(len(arg)):
            if not idx % 2:
                mocked = mocked + arg[idx].lower()
            else:
                mocked = mocked + arg[idx].upper()
        await ctx.send(mocked)
        await ctx.message.delete()

    @commands.command(help="Ping the bot")
    async def ping(self, ctx):
        await ctx.send("pong! 🏓")

    @commands.command(help="Repeat the given message")
    async def say(self, ctx):
        arg_message = discord_utils.extract_clean_message(ctx)
        if ctx.message.reference is not None:
            referencedMessage = await ctx.channel.fetch_message(
                ctx.message.reference.message_id
            )
            await referencedMessage.reply(arg_message)
        else:
            await ctx.send(arg_message)
        await ctx.message.delete()

    @commands.command(help="Zalgofy the given message")
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
