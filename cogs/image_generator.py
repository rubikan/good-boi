import discord
import replicate
import typing
import functools
import logging

from util import const
from discord.ext import commands
from discord.ext.commands import Context

_log = logging.getLogger(__name__)


async def run_blocking(
    client, blocking_func: typing.Callable, *args, **kwargs
) -> typing.Any:
    func = functools.partial(blocking_func, *args, **kwargs)
    return await client.loop.run_in_executor(None, func)


class ImageGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def generate(ctx: Context, prompt: str, model: str, **kwargs):
        _log.info(
            f"Generating image for prompt `{prompt} with model {model} and kwargs {kwargs}`..."
        )

        msg = await ctx.send(f"Generating image for prompt `{prompt}`...")
        async with ctx.typing():
            try:
                input = {"prompt": prompt, "aspect_ratio": "4:3"}

                output = await run_blocking(
                    ctx.bot,
                    replicate.run,
                    model,
                    input=input,
                )

                image_url = output.url

                embed = discord.Embed(title=prompt, color=const.EMBED_COLOR)
                embed.set_image(url=image_url)
                await msg.edit(
                    content=None,
                    embed=embed,
                )
            except Exception as e:
                _log.error(
                    f"Failed to generate image for prompt `{prompt}`. Reason: {e}"
                )
                await msg.edit(
                    content=f"Failed to generate image for prompt `{prompt}`. Reason: `{e}`"
                )

    @commands.command(aliases=["image"], help="Generate an open journey image")
    async def imagen(self, ctx, *, arg):
        await self.generate(ctx, arg, const.IMAGEN_MODEL, width=1024, height=768)


async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
