import discord

from discord.ext import commands
from util import const,data

class Static(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['fockin'])
    async def fuckin(self, ctx):
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            await message.reply(file = discord.File(data.get_audio_path(const.THEY_FOCKIN)))
        else:
            await ctx.send(file = discord.File(data.get_audio_path(const.THEY_FOCKIN)))
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Static(bot))