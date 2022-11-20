import discord
import replicate

from discord.ext import commands
from util import const


class ImageGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def generate(ctx, arg, model):
        msg = await ctx.send(f"Generating image for prompt `{arg}`...")
        async with ctx.typing():
            model = replicate.models.get(model)
            images = model.predict(prompt=arg)
            image = images[0]

            embed = discord.Embed(title=arg, color=const.EMBED_COLOR)
            embed.set_image(url=image)
            await msg.edit(
                content=None,
                embed=embed,
            )

    @commands.command(aliases=["oj"])
    async def openjourney(self, ctx, *, arg):
        await self.generate(ctx, arg, const.OJ_MODEL)

    @commands.command(aliases=["pkm"])
    async def pokemon(self, ctx, *, arg):
        await self.generate(ctx, arg, const.PKM_MODEL)


async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
