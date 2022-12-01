import asyncio
import discord

from async_timeout import timeout
from discord.ext import commands
from util import const, data, ytdlp

VOICE_CONNECTION_TIMEOUT = "I could not connect to that channel."
VOICE_NOT_CONNECTED = "I am not connected to a voice channel."
VOICE_NOT_PLAYING = "I am currently playing nothing."
VOICE_NOT_PAUSED = "There is nothing paused currently."
VOICE_ERROR = "There was an error 😔"

# 5 Minutes
TIMEOUT_AFTER = 300


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

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song ...
                async with timeout(TIMEOUT_AFTER):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                # ... run cleanup if we run into a timeout
                return self.destroy(self.guild)

            if not isinstance(source, ytdlp.YoutubeSource):
                # Regather stream to prevent stream expiration
                try:
                    source = await ytdlp.YoutubeSource.regather_stream(
                        source, loop=self.bot.loop
                    )
                except Exception as e:
                    await self.channel.send(VOICE_ERROR)
                    continue

            source.volume = self.volume
            self.current = source
            self.guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )
            embed = discord.Embed(
                title="Playing",
                description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]",
                color=const.EMBED_COLOR,
            )
            self.np = await self.channel.send(embed=embed)
            await self.next.wait()

            # Clean up the FFMPEG process
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        return self.bot.loop.create_task(self.cog.cleanup(guild))


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

    # GENERAL COMMANDS

    @commands.command(
        aliases=["connect"],
    )
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        await ctx.message.delete()
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

    @commands.command(
        aliases=["disconnect"],
    )
    async def leave(self, ctx):
        await ctx.message.delete()
        client = ctx.voice_client
        if not client or not client.is_connected():
            return await ctx.send(VOICE_NOT_CONNECTED)
        await self.cleanup(ctx.guild)

    # YOUTUBE COMMANDS

    @commands.command()
    async def play(self, ctx, *, query: str):
        await ctx.message.delete()
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)

        player = self.get_player(ctx)
        source = await ytdlp.YoutubeSource.create_source(
            ctx, query, loop=self.bot.loop, download=False
        )
        await player.queue.put(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.message.delete()
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)
            return
        if not client.is_playing():
            await ctx.send(VOICE_NOT_PLAYING)
            return
        if client.is_paused():
            return

        client.pause()
        await ctx.send("⏸️ Paused ⏸️")

    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete()
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)
            return
        if not client.is_paused():
            await ctx.send(VOICE_NOT_PAUSED)
            return

        client.resume()
        await ctx.send("⏯️ Resuming ⏯️")

    @commands.command()
    async def skip(self, ctx):
        await ctx.message.delete()
        client = ctx.voice_client
        if not client or not client.is_connected():
            await ctx.send(VOICE_NOT_CONNECTED)
            return
        if not client.is_playing():
            await ctx.send(VOICE_NOT_PLAYING)
            return

        client.stop()

    @commands.command()
    async def queue(self, ctx):
        await ctx.message.delete()
        return await ctx.send("Not implemented exception lol")

    # OTHER COMMANDS

    @commands.command()
    async def tts(self, ctx):
        await ctx.message.delete()
        return await ctx.send("Not implemented exception lol")
        client = ctx.voice_client
        resume = False
        if client.is_playing():
            client.pause()
            resume = True
        # TODO implement
        if resume:
            client.resume()

    # STATIC FILE COMMANDS

    async def play_static_file(self, ctx, audio_path):
        client = ctx.voice_client
        resume = False
        if client.is_playing():
            client.pause()
            resume = True
        # TODO TypeError: object NoneType can't be used in 'await' expression
        # Maybe we still need the duration of the mp3 played, since we can't await client.play
        await client.play(
            discord.FFmpegPCMAudio(executable="ffmpeg", source=audio_path)
        )
        if resume:
            client.resume()

    @commands.command(aliases=["fockin"])
    async def fuckin(self, ctx):
        await ctx.message.delete()
        await self.play_static_file(ctx, data.get_audio_path(const.THEY_FOCKIN))


async def setup(bot):
    await bot.add_cog(Music(bot))
