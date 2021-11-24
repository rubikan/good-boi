from discord.ext import commands

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command(aliases=['sfp'])
    async def shittyfoodporn(self, ctx):
        await ctx.send("NOT IMPLEMENTED LOLOLOL")

def setup(bot):
    bot.add_cog(Reddit(bot))