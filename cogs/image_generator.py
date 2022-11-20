from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import replicate

from util import const

MODEL = "prompthero/openjourney"
MODEL_VERSION = "9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb"


class ImageGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def generate(self, ctx: Context, *, arg: str):
        msg = await ctx.send(f"Generating image for prompt `{arg}`...")
        async with ctx.typing():
            model = replicate.models.get(MODEL)
            images = model.predict(prompt=arg)
            image = images[0]

            embed = Embed(title=arg, color=const.EMBED_COLOR)
            embed.set_image(url=image)
            await msg.edit(
                content=None,
                embed=embed,
            )


async def setup(bot):
    await bot.add_cog(ImageGenerator(bot))
