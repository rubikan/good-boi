import logging
import asyncio

import replicate
from discord.ext import commands

_log = logging.getLogger(__name__)


class AIChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tasks = {}

    @commands.command(
        help="Ask GoodBoi a question that will be answered using Deepseek"
    )
    async def chat(self, ctx, *, arg):
        msg_content = "I'm thinking..."
        msg = await ctx.reply(msg_content)

        task = asyncio.create_task(self._generate_response(ctx, arg, msg))
        self.active_tasks[ctx.channel.id] = task

        try:
            await task
        except asyncio.CancelledError:
            await msg.edit(content=msg_content + "\n\n**[Response stopped by user]**")
        finally:
            self.active_tasks.pop(ctx.channel.id, None)

    async def _generate_response(self, ctx, prompt, msg):
        async with ctx.typing():
            msg_content = ""
            input = {"prompt": prompt}
            for event in replicate.stream("deepseek-ai/deepseek-v3", input=input):
                if asyncio.current_task().cancelled():
                    break
                msg_content += event.data
                if len(msg_content) >= 2000:
                    msg_content = event.data
                    msg = await ctx.reply(msg_content)
                if len(msg_content) > 0:
                    await msg.edit(content=msg_content)

    @commands.command(help="Make GoodBoi shut up")
    async def stop(self, ctx):
        task = self.active_tasks.get(ctx.channel.id)
        if task and not task.done():
            task.cancel()


async def setup(bot):
    await bot.add_cog(AIChat(bot))
