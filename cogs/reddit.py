import discord
import requests

from util import const
from discord.ext import commands

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        try:
            permalink = const.REDDIT_TLD + json[1]["data"]["children"][0]["data"]["permalink"]
        except IndexError:
            permalink = img_url
        embed = discord.Embed(title=title, url=permalink, color=const.EMBED_COLOR)
        embed.set_image(url=img_url)

        return embed
     
    @commands.command(aliases=['sfp'])
    async def shittyfoodporn(self, ctx):
        post_json = self.get_from_reddit("shittyfoodporn", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dv'])
    async def disneyvacation(self, ctx):
        post_json = self.get_from_reddit("disneyvacation", "random", "1", "all")
        embed = self.create_image_embed(post_json)
        await ctx.send(embed=embed)        

def setup(bot):
    bot.add_cog(Reddit(bot))