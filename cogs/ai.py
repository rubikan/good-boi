import os
from openai import OpenAI
from discord.ext import commands


class AI(commands.Cog):
    client: OpenAI

    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            base_url=bot.config.openai.baseUrl,
            api_key=bot.config.openai.apiKey,
        )

    @commands.command()
    async def chat(self, ctx, *, arg):
        async with ctx.typing():
            result = self.client.chat.completions.create(
                model=self.bot.config.openai.model,
                messages=[
                    {"role": "system", "content": self.bot.config.openai.chatPrompt},
                    {"role": "user", "content": arg},
                ],
            )
            answer = result.choices[0].message.content
            await ctx.send(answer)


async def setup(bot):
    await bot.add_cog(AI(bot))
