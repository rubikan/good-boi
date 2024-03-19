import os
from openai import OpenAI
from discord.ext import commands


class AI(commands.Cog):
    client: OpenAI

    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            base_url=os.environ.get("OPENAI_BASE_URL"),
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    @commands.command()
    async def chat(self, ctx, arg):
        """Chat with the AI"""
        async with ctx.typing():
            result = self.client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": arg},
                ],
            )
            answer = result.choices[0].message.content
            await ctx.send(answer)
