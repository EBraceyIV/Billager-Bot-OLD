import discord
from discord.ext import commands
import shelve
import typing

# shelve init
plusMinus = shelve.open('plusMinus') # stores the +- scores

# This is here to use
beefBrain = '<:BeefBrain:631694337549271050>'


class Score(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Let users add to other users' scores
    @commands.command(name="+", help="Add to a user's score.",
                      description="This defaults to a +1, but any integer can be used for [int].")
    async def plus(self, ctx, num: typing.Optional[int] = 1, *, member: discord.Member):
        # Some in-command error catching, +- will only process integers
        try:
            # Prevent users from adding to their own score
            if str(member.mention) == str(ctx.message.author.mention):
                await ctx.send("Trying to boost your own numbers? Shameful.")
                return
            else:
                if member.mention not in plusMinus:
                    plusMinus[member.mention] = num
                else:
                    plusMinus[member.mention] = int(plusMinus[member.mention]) + num
                # com_term = self.bot.get_channel(461773779165511681)
                await ctx.send(str(member.display_name) + ' +' + str(num))

        except ValueError:
            await ctx.send('You can only add whole numbers' + beefBrain)

    # Let users subtract from other users' scores
    @commands.command(name="-", help="Subtract from a user's score.",
                      description="This defaults to a -1, but any integer can be used for [int].")
    async def minus(self, ctx, num: typing.Optional[int] = 1, *, member: discord.Member):
        # Some in-command error catching, +- will only process integers
        try:
            print(member.mention + ' -' + str(num))
            if member.mention not in plusMinus:
                plusMinus[member.mention] = -num
            else:
                plusMinus[member.mention] = int(plusMinus[member.mention]) - num
                print(member.mention + ' is up to ' + str(plusMinus[member.mention]))

            # com_term = self.bot.get_channel(461773779165511681)
            await ctx.send(str(member.display_name) + ' -' + str(num))

        except ValueError:
            await ctx.send('You can only subtract whole numbers ' + beefBrain)

    # Respond with the specified user's score
    @commands.command(name="score", aliases=['Score', 'SCORE'], help="List a user's +- score.")
    async def score(self, ctx, member: discord.Member):
        # Initialize user's score if they don't already have one
        if member.mention not in plusMinus:
            plusMinus[member.mention] = int(0)
        print(member.display_name + ' is at a ' + str(plusMinus[member.mention]))
        await ctx.send(member.display_name + ' is at a ' + str(plusMinus[member.mention]))

    # Show a scoreboard from highest to lowest for all users with a score
    @commands.command(name="scoreboard", aliases=["Scoreboard"], help="Scoreboard of the highest and lowest scores.")
    async def scoreboard(self, ctx):
        # Initialize scoreboard embed message and embed description
        embed = discord.Embed(title="Scoreboard")
        desc = ""
        # Sort the current user scores from highest to lowest
        score_sorted = sorted(plusMinus.items(), key=lambda x: x[1])
        # Iterate through the scores and build the embed content
        for score in score_sorted:
            # Here "score" is a tuple, containing the user and score, adding each to a new line
            desc = str(score[0]) + ": " + str(score[1]) + "\n" + desc
        # Add some flavor text and send the message
        embed.description = "Here's the current scoreboard. Honestly can't believe these numbers: \n\n" + desc
        embed.set_footer(text="Be sure to use bb:+ and bb:- to our keep scoreboard up to date.")
        await ctx.send(embed=embed)

    # Some general error processing for some of the score commands

    @plus.error
    @minus.error
    async def plus_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("You can't do that " + beefBrain)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You forgot to give me a name ' + beefBrain)

    @score.error
    async def score_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You forgot to give me a name ' + beefBrain)


def setup(bot):
    bot.add_cog(Score(bot))
