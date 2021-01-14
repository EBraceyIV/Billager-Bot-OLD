from discord.ext import commands


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # A more advanced method to fixing any issues with the voice chat functionality, reloads the whole cog
    @commands.command(name="vreload", hidden=True)
    async def vreload(self, ctx):
        self.bot.reload_extension("cogs.voice")
        await ctx.send("Reloaded voice cog.")


'''
  @commands.command()
async def score_reply(self, ctx, channel: discord.TextChannel):
    print(channel)
    score_channel = channel
    await ctx.send('Score outputs will be sent to ' + str(score_channel))
'''


def setup(bot):
    bot.add_cog(settings(bot))
