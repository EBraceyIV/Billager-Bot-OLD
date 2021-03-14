import discord
from discord.ext import commands
import json

validOutputs = ["callout"]
discord_activity_types = {"playing": discord.ActivityType.playing,
                          "listening": discord.ActivityType.listening,
                          "watching": discord.ActivityType.watching,
                          "competing": discord.ActivityType.competing}


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="presence")
    async def presence(self, ctx, activity_type, *, activity):
        if activity_type not in discord_activity_types:
            await ctx.send("That is not a valid activity type. I only accept \"playing\", \"listening\", \"watching\", "
                           "or \"competing\". The food basic food groups of having fun.")
        for discord_activity_type in discord_activity_types.keys():
            if activity_type == discord_activity_type:
                activity_type = discord_activity_types[activity_type]
        await self.bot.change_presence(activity=discord.Activity(type=activity_type, name=activity))

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
    async def outputs_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing the output label or the designated channel, try again.")

    @presence.error
    async def presence_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You're missing the activity type or activity description, try again.")


def setup(bot):
    bot.add_cog(Settings(bot))
