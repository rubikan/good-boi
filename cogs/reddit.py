import discord
import requests
import re

from util import const
from discord.ext import commands

IMGUR_REGEX = re.compile("https://imgur.com/([A-z0-9]+)")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def map_imgur_url(url: str) -> str:
        matches = IMGUR_REGEX.findall(url)
        if len(matches) == 0:
            return url
        else:
            return f"https://i.imgur.com/{matches[0]}.jpg"

    @staticmethod
    def get_from_reddit(subreddit, listing, count, timeframe):
        """
        Calls the reddit api and returns posts as json

        Args:
            subreddit: From which subreddit should the posts be fetched
            listing: Which listing should be used (controversial, best, hot, new, random, rising, top)
            count: How many posts should be fetched
            timeframe: From which timeframe should the posts be fetched (hour, day, week, month, year, all)

        Returns:
            Result of the reddit api call as json
        """
        try:
            call_url = const.REDDIT_API.format(subreddit=subreddit, listing=listing, count=count, timeframe=timeframe)
            request = requests.get(call_url, headers=const.REQUEST_HEADERS)
        except Exception as e:
            print(f"Error calling {call_url}. Reason: ", e)
        return request.json()

    @staticmethod
    def create_image_embed(json):
        """
        Creates an embed containing an image from the given reddit json. Only works if the title, url_overridden_by_dest and permalink attributes are present
        """
        title = json[0]["data"]["children"][0]["data"]["title"]
        img_url = json[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]
        img_url = Reddit.map_imgur_url(img_url)

        subreddit = json[0]["data"]["children"][0]["data"]["subreddit"]
        post_id = json[0]["data"]["children"][0]["data"]["id"]
        post_link = const.REDDIT_POST_LINK.format(subreddit=subreddit, id=post_id)

        embed = discord.Embed(title=title, url=post_link, color=const.EMBED_COLOR)
        embed.set_image(url=img_url)

        return embed

    @commands.command(aliases=['abd'])
    async def animalsbeingderps(self, ctx):
        post_json = self.get_from_reddit("AnimalsBeingDerps", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dem'])
    async def dallemini(self, ctx):
        post_json = self.get_from_reddit("dallemini", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['dv'])
    async def disneyvacation(self, ctx):
        post_json = self.get_from_reddit("disneyvacation", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

    @commands.command(aliases=['irl'])
    async def me_irl(self, ctx):
        post_json = self.get_from_reddit("me_irl", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ph'])
    async def programmerhumor(self, ctx):
        post_json = self.get_from_reddit("ProgrammerHumor", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)
     
    @commands.command(aliases=['sfp'])
    async def shittyfoodporn(self, ctx):
        post_json = self.get_from_reddit("shittyfoodporn", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

    @commands.command(aliases=['wwp'])
    async def wewantplates(self, ctx):
        post_json = self.get_from_reddit("WeWantPlates", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reddit(bot))