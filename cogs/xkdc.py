import random
import requests

from util import const
from bs4 import BeautifulSoup
from discord.ext import commands

class XKDC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_newest_link():
        page = requests.get(const.XKDC_URL, headers=const.REQUEST_HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        containerDiv = soup.find("div", {"id": "middleContainer"})   
        containerChildren = containerDiv.findChildren("a") 
        for child in containerChildren:
            if (child["href"].startswith(const.XKDC_URL)):
                return child["href"]

    @staticmethod
    def get_newest_id(self):
        newest_link = self.get_newest_link()
        return int(newest_link.rsplit('/', 1)[-1])

    @staticmethod
    def get_random_link(self):
        rand_int = random.randint(1, self.get_newest_id(self))
        return const.XKDC_URL + str(rand_int)

    @commands.command()
    async def xkdc(self, ctx, argument = None):
        if argument == None:
            await ctx.send(self.get_newest_link())
        elif argument.lower() == "random":
            await ctx.send(self.get_random_link(self))
        elif argument.isdigit() and 1 <= int(argument) <= self.get_newest_id(self):
            await ctx.send(const.XKDC_URL + argument)

def setup(bot):
    bot.add_cog(XKDC(bot))