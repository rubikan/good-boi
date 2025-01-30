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
                input = {
                    "prompt": prompt,
                    "scheduler": kwargs.get("scheduler") or "K_EULER",
                    "width": kwargs.get("width") or 1024,
                    "height": kwargs.get("height") or 1024,
                    "guidance_scale": kwargs.get("guidance_scale") or 3,
                    "negative_prompt": "ugly, deformed, noisy, blurry, distorted",
                    "num_inference_steps": kwargs.get("num_inference_steps") or 25,
                }

                output = await run_blocking(
                    ctx.bot,
                    replicate.run,
                    model,
                    input=input,
                )

                if type(output) == list:
                    image = output[0]
                # it's a generator?
                else:
                    image = next(output)

                embed = discord.Embed(title=prompt, color=const.EMBED_COLOR)
                embed.set_image(url=image)
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

    @commands.command(aliases=["oj"], help="Generate an open journey image")
    async def openjourney(self, ctx, *, arg):
        await self.generate(ctx, arg, const.OJ_MODEL, width=1024, height=768)

    @commands.command(aliases=["pkm"], help="Generate a pokemon image")
    async def pokemon(self, ctx, *, arg):
        await self.generate(ctx, arg, const.PKM_MODEL)

    @commands.command(aliases=["sd"], help="Generate a stable diffusion image")
    async def stable_diffusion(self, ctx, *, arg):
        await self.generate(ctx, arg, const.SD_MODEL)

    @commands.command(aliases=["pg"], help="Generate a playground image")
    async def playground(self, ctx, *, arg):
        await self.generate(ctx, arg, const.PG_MODEL, scheduler="DPMSolver++")


async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
