import requests

from util import ascii_hangman, const, discord_utils
from discord.ext import commands


class HangmanState:
    def __init__(self):
        self.word = requests.get(
            const.RANDOM_WORD_API, headers=const.REQUEST_HEADERS
        ).json()[0]
        self.guessedLetters = list()
        self.wrongGuesses = 0

    def currentWordState(self):
        currentWordState = self.word
        for char in currentWordState:
            if not char in self.guessedLetters:
                currentWordState = currentWordState.replace(char, "_")
        return f"```{" ".join(currentWordState)}```"

    def currentGuessedLetters(self):
        return f"```Guessed letters: {self.guessedLetters}```"

    def guess(self, char):
        char = char.lower()
        self.guessedLetters.append(char)
        if char in self.word:
            return True
        else:
            self.wrongGuesses += 1
            return False

    def guessWord(self, guessedWord):
        if guessedWord == self.word:
            return True
        else:
            self.wrongGuesses += 1
            return False

    def ascii(self):
        return ascii_hangman.PIC[self.wrongGuesses]


class Hangman(commands.Cog):
    gameCache = {}

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def uid(ctx):
        return ctx.message.author.id

    @staticmethod
    async def printState(self, ctx):
        game_state = Hangman.gameCache[self.uid(ctx)]
        await ctx.send(game_state.ascii())
        await ctx.send(game_state.currentGuessedLetters())
        await ctx.send(game_state.currentWordState())

    @commands.group(aliases=["hm"], help="Play hangman", invoke_without_command=True)
    async def hangman(self, ctx):
        await ctx.send("Subcommand not found")

    @hangman.command(help="Starts a game of hangman")
    async def start(self, ctx):
        if self.uid(ctx) in Hangman.gameCache:
            await ctx.send("We already have a game running!")
            await self.printState(self, ctx)
        else:
            Hangman.gameCache[self.uid(ctx)] = HangmanState()
            await self.printState(self, ctx)

    @hangman.command(help="Stops currently running game of hangman for user")
    async def stop(self, ctx):
        if self.uid(ctx) in Hangman.gameCache:
            await ctx.send(f"THE SOLUTION WAS: {Hangman.gameCache[self.uid(ctx)].word}")
            del Hangman.gameCache[self.uid(ctx)]
        else:
            await ctx.send("We don't have a game running!")

    @hangman.command(
        aliases=["g"], help="Guess a letter or the whole word for your hangman game"
    )
    async def guess(self, ctx):
        if self.uid(ctx) in Hangman.gameCache:
            game_state = Hangman.gameCache[self.uid(ctx)]
            arg = discord_utils.extract_clean_message(ctx)
            if len(arg) > 1:
                if game_state.guessWord(arg):
                    await ctx.send("CORRECT! YOU WIN!")
                    del Hangman.gameCache[self.uid(ctx)]
                    return
                else:
                    await ctx.send("WRONG GUESS!")
                    await self.printState(self, ctx)
            else:
                if game_state.guess(arg):
                    await ctx.send("CORRECT GUESS!")
                else:
                    await ctx.send("WRONG GUESS!")
            if game_state.wrongGuesses < 6:
                await self.printState(self, ctx)
            else:
                await ctx.send(game_state.ascii())
                await ctx.send("YOU LOST!")
                await ctx.send(f"THE SOLUTION WAS: {game_state.word}")
                del Hangman.gameCache[self.uid(ctx)]
        else:
            await ctx.send("We don't have a game running!")


async def setup(bot):
    await bot.add_cog(Hangman(bot))
