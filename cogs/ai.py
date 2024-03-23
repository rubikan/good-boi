from dataclasses import dataclass
from openai import OpenAI
from discord.ext.commands import Context
from discord.ext import commands
import logging
from abc import ABC

EDIT_EVERY_N_CHARS = 20
LENGTH_THRESHOLD = 1500

_log = logging.getLogger(__name__)


class ChunkResult(ABC):
    pass


@dataclass
class EditExistingMessage(ChunkResult):
    chunk: str


@dataclass
class CreateNewMessage(ChunkResult):
    old_message_chunk: str
    new_message_chunk: str


def handle_chunk(message_so_far: str, new_content: str) -> ChunkResult:
    new_len = len(new_content) + len(message_so_far)
    if new_len > LENGTH_THRESHOLD and "\n" in new_content:
        [start, rest] = new_content.split("\n", 1)
        return CreateNewMessage(start, rest)
    else:
        return EditExistingMessage(new_content)


class AI(commands.Cog):
    client: OpenAI

    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            base_url=bot.config.openai.base_url,
            api_key=bot.config.openai.api_key,
        )

    @commands.command(help="Talk to an AI chatbot")
    async def chat(self, ctx: Context, *, arg: str):
        msg = await ctx.reply("I'm thinking...")
        async with ctx.typing():
            result = self.client.chat.completions.create(
                model=self.bot.config.openai.model,
                messages=[
                    {"role": "system", "content": self.bot.config.openai.chat_prompt},
                    {"role": "user", "content": arg},
                ],
                stream=True,
                temperature=0.7,
                max_tokens=4000,
            )
            answer = ""
            delta_len = 0
            for chunk in result:
                content = chunk.choices[0].delta.content
                if content:
                    action = handle_chunk(message_so_far=answer, new_content=content)
                    _log.info(f"Action: {action}")

                    if isinstance(action, EditExistingMessage):
                        answer += action.chunk
                        delta_len += len(action.chunk)
                        if delta_len > EDIT_EVERY_N_CHARS:
                            await msg.edit(content=answer)
                            delta_len = 0
                    elif isinstance(action, CreateNewMessage):
                        answer += action.old_message_chunk
                        await msg.edit(content=answer)
                        answer = action.new_message_chunk

                        reply_text = answer
                        if reply_text.strip() == "":
                            reply_text = "I'm thinking..."
                        msg = await msg.reply(reply_text)

            # if any content was left over
            if delta_len > 0:
                await msg.edit(content=answer)


async def setup(bot):
    await bot.add_cog(AI(bot))
