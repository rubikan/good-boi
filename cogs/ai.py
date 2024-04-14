from dataclasses import dataclass
import requests
import json
from discord.ext.commands import Context
from discord.ext import commands
import logging
from abc import ABC
from sseclient import SSEClient

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


stop_sequences = ["You:", "\nYou ", "\nKoboldAI: "]

request_defaults = {
    "n": 1,
    "max_context_length": 4096,
    "max_length": 512,
    "rep_pen": 1.1,
    "temperature": 0.59,
    "top_p": 1,
    "top_k": 0,
    "top_a": 0,
    "typical": 1,
    "tfs": 0.87,
    "rep_pen_range": 1600,
    "rep_pen_slope": 0.3,
    "sampler_order": [6, 5, 0, 2, 3, 1, 4],
    "memory": "",
    "genkey": "KCPP1388",
    "min_p": 0,
    "dynatemp_range": 0,
    "dynatemp_exponent": 1,
    "smoothing_factor": 0,
    "presence_penalty": 0,
    "logit_bias": {},
    "quiet": True,
    "stop_sequence": stop_sequences,
    "use_default_badwordsids": False,
}


class KoboldApi:
    base_url: str
    system_prompt: str

    def __init__(self, base_url: str, system_prompt: str):
        self.base_url = base_url
        self.system_prompt = system_prompt

    def get_completions(
        self,
        prompt: str,
        temperature=0.59,
    ):
        request_body = request_defaults.copy()
        request_body.update(
            {
                "temperature": temperature,
                "prompt": self.system_prompt.format(prompt=prompt),
            }
        )
        _log.info(f"Request body: {request_body}")
        response = requests.post(
            f"{self.base_url}/api/extra/generate/stream", json=request_body, stream=True
        )
        client = SSEClient(response)
        for event in client.events():
            parsed = json.loads(event.data)
            yield parsed["token"]


class AI(commands.Cog):
    client: KoboldApi

    def __init__(self, bot):
        self.bot = bot
        self.client = KoboldApi(
            bot.config.openai.base_url, bot.config.openai.chat_prompt
        )

    @commands.command(help="Talk to an AI chatbot")
    async def chat(self, ctx: Context, *, arg: str):
        msg = await ctx.reply("I'm thinking...")
        async with ctx.typing():
            result = self.client.get_completions(arg)
            answer = ""
            delta_len = 0
            for content in result:
                if content:
                    _log.debug(f"Content: '{content}'")
                    action = handle_chunk(message_so_far=answer, new_content=content)
                    _log.debug(f"Action: {action}")

                    matching_sequences = [
                        seq for seq in stop_sequences if answer.endswith(seq)
                    ]
                    if len(matching_sequences) > 0:
                        _log.info(
                            f"Stop sequence(s) {matching_sequences} detected, stopping chat"
                        )
                        break

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
