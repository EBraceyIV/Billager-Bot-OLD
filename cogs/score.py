import discord
from discord.ext import commands
import shelve

# shelve inits
pmFile = shelve.open('plusMinus') #stores the +- scores

beefBrain = '<:BeefBrain:631694337549271050>'


class Score(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="+", help="Add to a user's score.")
    async def plus(self, ctx, num: int, member: discord.Member):
        try:
            print(member.mention + ' +' + str(num))
            if member.mention not in pmFile:
                pmFile[member.mention] = num
            else:
                pmFile[member.mention] = int(pmFile[member.mention]) + num
                print(member.mention + ' is up to ' + str(pmFile[member.mention]))

            com_term = self.bot.get_channel(461773779165511681)
            await com_term.send(str(member.display_name) + ' +' + str(num))

        except ValueError:
            await ctx.send('You can only add numbers' + beefBrain)

    @commands.command(name="-", help="Subtract from a user's score.")
    async def minus(self, ctx, num: int, member: discord.Member):
        try:
            print(member.mention + ' -' + str(num))
            if member.mention not in pmFile:
                pmFile[member.mention] = -num
            else:
                pmFile[member.mention] = int(pmFile[member.mention]) - num
                print(member.mention + ' is up to ' + str(pmFile[member.mention]))

            com_term = self.bot.get_channel(461773779165511681)
            await com_term.send(str(member.display_name) + ' -' + str(num))

        except ValueError:
            await ctx.send('You can only subtract numbers ' + beefBrain)

    @commands.command(name="score", aliases=['Score', 'SCORE'], help="List a user's +- score.")
    async def score(self, ctx, member: discord.Member):
        if member.mention not in pmFile:
            pmFile[member.mention] = int(0)
        print(member.display_name + ' is at a ' + str(pmFile[member.mention]))
        await ctx.send(member.display_name + ' is at a ' + str(pmFile[member.mention]))

    @commands.command(name="scoreboard", aliases=["Scoreboard"], help="Scoreboard of the highest and lowest scores.")
    async def scoreboard(self, ctx):
        embed = discord.Embed(title="Scoreboard")
        score_sorted = sorted(pmFile.items(), key=lambda x: x[1])
        print(score_sorted[0][0])
        try:
            embed.add_field(name="High Score", value=score_sorted[0][0] + ": " + str(score_sorted[0][1]) + "\n" +
                                                     score_sorted[1][0] + ": " + str(score_sorted[1][1]) + "\n")
            embed.add_field(name="Low score", value=score_sorted[-1][0] + ": " + str(score_sorted[-1][1]) + "\n" +
                                                     score_sorted[-2][0] + ": " + str(score_sorted[-2][1]) + "\n")
        except IndexError:
            await ctx.send("OUCH! WHY?")
        else:
            await ctx.send(embed=embed)

    @plus.error
    async def plus_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('That\'s not a number ' + beefBrain)

    @minus.error
    async def minus_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('That\'s not a number ' + beefBrain)

    @score.error
    async def score_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You forgot to give me a name ' + beefBrain)


def setup(bot):
    bot.add_cog(Score(bot))
