import asyncio
import discord

from discord.ext import commands
from util import ytdlp

VOICE_CONNECTION_TIMEOUT = "I could not connect to that channel."
VOICE_NOT_CONNECTED = "I am not connected to a voice channel."
VOICE_NOT_PLAYING = "I am currently playing nothing."


class YoutubePlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.now_playing = None
        self.volume = 0.5
        self.current = None
        ctx.bot.loop.create_task(self.loop())

    async def loop(self):
        await self.bot.wait_until_ready()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_player(self, ctx):
        if ctx.guild.id in self.players:
            return self.players[ctx.guild.id]

        player = YoutubePlayer(ctx)
        self.players[ctx.guild.id] = player

        return player

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    @commands.command()
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        if channel is None:
            channel = ctx.author.voice.channel

        client = ctx.voice_client
        if client:
            if client.channel.id == channel.id:
                return
            try:
                await client.move_to(channel)
            except asyncio.TimeoutError:
                await ctx.send(VOICE_CONNECTION_TIMEOUT)
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                await ctx.send(VOICE_CONNECTION_TIMEOUT)
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query: str):
        await ctx.trigger_typing()

        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)

        player = self.get_player(ctx)
        source = await ytdlp.YTDLSource.create_source(
            ctx, query, loop=self.bot.loop, download=False
        )
        await player.queue.put(source)

    @commands.command()
    async def pause(self, ctx):
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)
        if not client.is_playing():
            await ctx.send(VOICE_NOT_PLAYING)
        if client.is_paused():
            return

        client.pause()
        await ctx.send("⏸️ Paused ⏸️")

    @commands.command()
    async def resume(self, ctx):
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)
        if not client.is_paused():
            return

        client.resume()
        await ctx.send("⏯️ Resuming ⏯️")


async def setup(bot):
    await bot.add_cog(Music(bot))
