from openai import OpenAI
from discord.ext.commands import Context
from discord.ext import commands


class AI(commands.Cog):
    client: OpenAI

    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(
            base_url=bot.config.openai.base_url,
            api_key=bot.config.openai.api_key,
        )

    @commands.command()
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
            )
            answer = ""
            delta_len = 0
            for chunk in result:
                content = chunk.choices[0].delta.content
                if content:
                    print("delta countent:", content)
                    answer += content
                    delta_len += len(content)
                    if delta_len > 5:
                        print("delta_len:", delta_len)
                        await msg.edit(content=answer)
                        delta_len = 0


async def setup(bot):
    await bot.add_cog(AI(bot))
