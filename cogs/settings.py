from discord.ext import commands


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


'''
  @commands.command()
async def score_reply(self, ctx, channel: discord.TextChannel):
    print(channel)
    score_channel = channel
    await ctx.send('Score outputs will be sent to ' + str(score_channel))
'''


def setup(bot):
    bot.add_cog(settings(bot))
