from discord.ext import commands
import json

validOutputs = ["callout"]


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Setting up some framework for a more modular way of defining which channels certain outputs go to
    #
    # Dealing with reading and writing to JSON files for settings
    @commands.command(name="outputs", hidden=True)
    async def outputs(self, ctx, output, channel):
        if output not in validOutputs:
            await ctx.send("That is not a valid output label. Valid output labels are: " + str(validOutputs))
        with open("output.json", "w") as outputJSON:
            json.dump({output: channel}, outputJSON)

    @commands.command(name="consoleJSON", hidden=True)
    async def json(self, ctx):
        with open("output.json") as f:
            print(json.load(f))

    # A more advanced method to fixing any issues with the voice chat functionality, reloads the whole cog
    @commands.command(name="vreload", hidden=True)
    async def vreload(self, ctx):
        self.bot.reload_extension("cogs.voice")
        await ctx.send("Reloaded voice cog.")

    @outputs.error
    async def score_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing the output label or the designated channel, try again.")


def setup(bot):
    bot.add_cog(Settings(bot))
