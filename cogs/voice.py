import discord

from discord.ext import commands
from util import const, data, text


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def play_file(ctx, file):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=file))
        except:
            await ctx.send(text.VOICE_NOT_CONNECTED)

    @commands.command()
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        if channel is None:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["fockin"])
    async def fuckin(self, ctx):
        file = discord.File(data.get_audio_path(const.THEY_FOCKIN))
        await self.play_file(ctx, file)


async def setup(bot):
    await bot.add_cog(Voice(bot))
