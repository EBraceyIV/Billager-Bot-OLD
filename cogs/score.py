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
        # Some in-command error catching, +- will only process integers
        try:
            # Prevent users from adding to their own score
            if str(member.mention) == str(ctx.message.author.mention):
                await ctx.send("Trying to boost your own numbers? Shameful.")
                return
            else:
                if member.mention not in pmFile:
                    pmFile[member.mention] = num
                else:
                    pmFile[member.mention] = int(pmFile[member.mention]) + num
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
        # Initialize scoreboard embed message and embed description
        embed = discord.Embed(title="Scoreboard")
        desc = ""
        # Sort the current user scores from highest to lowest
        score_sorted = sorted(pmFile.items(), key=lambda x: x[1])
        # Iterate through the scores and build the embed content
        for score in score_sorted:
            # Here "score" is a tuple, containing the user and score, adding each to a new line
            desc = str(score[0]) + ": " + str(score[1]) + "\n" + desc
        # Add some flavor text and send the message
        embed.description = "Here's the current scoreboard. Honestly can't believe these numbers: \n\n" + desc
        embed.set_footer(text="Be sure to use bb:+ and bb:- to our keep scoreboard up to date.")
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
