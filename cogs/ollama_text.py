import os
import logging

from util import const
from ollama import AsyncClient
from discord.ext import commands

_log = logging.getLogger(__name__)


class OllamaText(commands.Cog):
    ollama_client: AsyncClient

    def __init__(self, bot):
        self.bot = bot
        ollama_url: str
        if "GOODBOI_OLLAMA_URL" in os.environ:
            ollama_url = os.environ["GOODBOI_OLLAMA_URL"]
        else:
            ollama_url = "http://good-boi-ollama:11434"
        self.ollama_client = AsyncClient(
            host=ollama_url,
        )

    @commands.command(help="Ask GoodBoi a question that will be answered using Ollama")
    async def ask(self, ctx, *, arg):
        _log.info(f"Prompting ollama `{arg} with model {const.OLLAMA_TXT_MODEL}`...")
        ollama_prompt = {"role": "user", "content": arg}

        msg_content = "I'm thinking..."
        msg = await ctx.reply(msg_content)
        async with ctx.typing():
            msg_content = ""
            async for part in await AsyncClient().chat(
                model=const.OLLAMA_TXT_MODEL, messages=[ollama_prompt], stream=True
            ):
                msg_content += part["message"]["content"]
                await msg.edit(content=msg_content)
            # TODO: message cutoff at 1500, begin new message, check why this is slow a.f., deepseek-r1:32b is not the best model either

        response = self.ollama_client.chat(
            model=const.OLLAMA_TXT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": arg,
                },
            ],
        )
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(OllamaText(bot))
