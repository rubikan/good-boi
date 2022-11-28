import discord

from discord.ext import commands
from util import const, data

VOICE_NOT_CONNECTED = "I am not connected to a voice channel."


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def play_file(ctx, file_path):
        server = ctx.message.guild
        voice_channel = server.voice_client
        if voice_channel is None:
            await ctx.send(VOICE_NOT_CONNECTED)
        else:
            voice_channel.play(
                discord.FFmpegPCMAudio(executable="ffmpeg", source=file_path)
            )

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
        file_path = data.get_audio_path(const.THEY_FOCKIN)
        await self.play_file(ctx, file_path)


async def setup(bot):
    await bot.add_cog(Voice(bot))
