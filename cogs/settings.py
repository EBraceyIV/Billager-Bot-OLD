from discord.ext import commands
import json


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Setting up some framework for a more modular way of defining which channels certain outputs go to
    #
    # Dealing with reading and writing to JSON files for settings
    @commands.command(name="calloutChannel", hidden=True)
    async def calloutChannel(self, ctx, channel):
        with open("callout.json", "w") as json_file:
            json.dump({"callout_channel": channel}, json_file)

    @commands.command(name="json", hidden=True)
    async def json(self, ctx):
        with open("callout.json") as f:
            print(json.load(f))

    # A more advanced method to fixing any issues with the voice chat functionality, reloads the whole cog
    @commands.command(name="vreload", hidden=True)
    async def vreload(self, ctx):
        self.bot.reload_extension("cogs.voice")
        await ctx.send("Reloaded voice cog.")


def setup(bot):
    bot.add_cog(settings(bot))
