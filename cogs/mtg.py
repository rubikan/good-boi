import discord
import logging
import nest_asyncio
import scrython

from util import const
from discord.ext import commands

_log = logging.getLogger(__name__)

class Mtg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scry(self, ctx, *, arg):
        try:
            nest_asyncio.apply()
            card = scrython.cards.Named(fuzzy=arg)

            if card.object() == 'error':
                await ctx.send(card.scryfallJson['details'])

            cardEmbed = discord.Embed(title=card.name(), url=card.scryfall_uri(), color=const.EMBED_COLOR)
            _log.info("Image URI: " + card.image_uris(image_type="png"))
            cardEmbed.set_image(url=card.image_uris(image_type="png"))
            await ctx.send(embed=cardEmbed)
        except Exception as e:
            _log.error(f"There was an error communicating with the Scryfall API. Reason: ", str(e))
            await ctx.send(str(e))


async def setup(bot):
    await bot.add_cog(Mtg(bot))