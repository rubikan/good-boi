from openai import OpenAI
from discord.ext.commands import Context
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
    async def chat(self, ctx: Context, *, arg: str):
        msg = await ctx.send("Generating answer...")
        async with ctx.typing():
            result = self.client.chat.completions.create(
                model=self.bot.config.openai.model,
                messages=[
                    {"role": "system", "content": self.bot.config.openai.chatPrompt},
                    {"role": "user", "content": arg},
                ],
                stream=True,
            )
            answer = ""
            for chunk in result:
                content = chunk.choices[0].delta.content
                if content:
                    answer += content
                    msg.edit(content=answer)


async def setup(bot):
    await bot.add_cog(AI(bot))
