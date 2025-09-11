import logging

import replicate
from discord.ext import commands

_log = logging.getLogger(__name__)


class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Ask GoodBoi a question that will be answered using Deepseek"
    )
    async def chat(self, ctx, *, arg):
        msg_content = "I'm thinking..."
        msg = await ctx.reply(msg_content)
        async with ctx.typing():
            msg_content = ""
            input = {"prompt": arg}
            for event in replicate.stream("deepseek-ai/deepseek-v3", input=input):
                msg_content += event.data
                if len(msg_content) > 0:
                    await msg.edit(content=msg_content)


async def setup(bot):
    await bot.add_cog(AIChat(bot))
