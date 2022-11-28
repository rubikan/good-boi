import random
import requests

from util import const
from bs4 import BeautifulSoup
from discord.ext import commands


class Explosm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_random_page():
        page = requests.get(const.EXPLOSM_LATEST, headers=const.REQUEST_HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        rand_int = random.randint(1, const.EXPLOSM_RANDOM_UPPER_LIMIT)
        for i in range(rand_int):
            selectContainerDiv = soup.find(
                "div", {"class": const.EXPLOSM_SELECT_CONTAINER}
            )
            random_url = selectContainerDiv.select("div > a")[1]["href"]
            page = requests.get(
                const.EXPLOSM_URL + random_url, headers=const.REQUEST_HEADERS
            )
            soup = BeautifulSoup(page.content, "html.parser")

        return soup

    @staticmethod
    def extract_comic_url(soup: BeautifulSoup):
        comicContainerDiv = soup.find("div", {"class": const.EXPLOSM_COMIC_CONTAINER})
        imgTag = comicContainerDiv.findChild("img")
        return imgTag["src"]

    @commands.command(aliases=["c&h", "cah"])
    async def explosm(self, ctx):
        msg = await ctx.send("Getting a random explosm comic")
        async with ctx.typing():
            random_page = self.get_random_page()
            comic_url = self.extract_comic_url(random_page)
            await msg.edit(comic_url)


async def setup(bot):
    await bot.add_cog(Explosm(bot))
