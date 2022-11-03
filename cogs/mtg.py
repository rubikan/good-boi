import discord
import scrython

from util import const, text
from discord.ext import commands

class Mtg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scry(self, ctx, subcmd, argument):
        match subcmd:
            case "cards":
                self.cards(self, ctx, argument)
            case _:
                await ctx.send(text.UNKNOWN_COMMAND)

    async def cards(self, ctx, argument):
        card = scrython.cards.Named(fuzzy=argument)

        if card.object() == 'error':
            await ctx.send(card.scryfallJson['details'])

        cardEmbed = discord.Embed(title=card.name(), url=card.scryfall_uri, color=const.EMBED_COLOR)
        cardEmbed.set_image(url=card.image_uris[0])
        await ctx.send(embed=cardEmbed)

def setup(bot):
    bot.add_cog(Mtg(bot))