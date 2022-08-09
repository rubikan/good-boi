import random
import re
import requests

from bs4 import BeautifulSoup
from discord.ext import commands

XKDC_URL = "https://xkcd.com/"

class XKDC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_newest_link():
        page = requests.get(XKDC_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find(text="Permanent link to this comic: ").findNext("a")["href"]

    @staticmethod
    def get_newest_id(self):
        newest_link = self.get_newest_link()
        m = re.search(r'/(\d+)$/', newest_link)
        return int(m.group())

    @staticmethod
    def get_random_link(self):
        rand_int = random.randint(1, self.get_newest_id())
        return XKDC_URL + str(rand_int)

    @commands.command()
    async def xkdc(self, ctx, argument = None):
        if argument == None:
            await ctx.send(self.get_newest_link())
        elif argument.lower() == "random":
            await ctx.send(self.get_random_link())
        else:
            try:
                # Just check if its a number
                int(argument)
                await ctx.send(XKDC_URL + argument)
            except ValueError:
                await ctx.send(argument + " is not a valid number you simpleton!")

def setup(bot):
    bot.add_cog(XKDC(bot))