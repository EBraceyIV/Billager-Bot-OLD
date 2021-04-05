import discord
from discord.ext import commands
import shelve
import typing

# Initialize the scoreboard list of all currently scored members
scores = shelve.open("plusMinus")
scored_members = list(scores.keys())
scores.close()


# Member score management function
#   action: Add to or subtract from a score, or see what the score is
#   member: Which user's score to manage
#   amount: What score to add/remove
def score_func(action, member, amount):
    global scored_members
    plus_minus = shelve.open("plusMinus")
    if action == "init":
        plus_minus[member] = amount
    elif action == "add":
        plus_minus[member] = plus_minus.get(member) + amount
    elif action == "get":
        return plus_minus.get(member)
    elif action == "subtract":
        plus_minus[member] = plus_minus.get(member) - amount
    scored_members = list(plus_minus.keys())
    plus_minus.close()


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
                if member.mention not in scored_members:
                    score_func("init", member.mention, num)
                else:
                    score_func("add", member.mention, num)
                await ctx.reply(str(member.display_name) + ' +' + str(num), mention_author=False)

        except ValueError:
            await ctx.send('You can only add whole numbers' + beefBrain)

    # Let users subtract from other users' scores
    @commands.command(name="-", help="Subtract from a user's score.",
                      description="This defaults to a -1, but any integer can be used for [int].")
    async def minus(self, ctx, num: typing.Optional[int] = 1, *, member: discord.Member):
        # Some in-command error catching, +- will only process integers
        try:
            if member.mention not in scored_members:
                score_func("init", member.mention, -num)
            else:
                score_func("subtract", member.mention, num)
            await ctx.reply(str(member.display_name) + ' -' + str(num), mention_author=False)

        except ValueError:
            await ctx.send('You can only subtract whole numbers ' + beefBrain)

    # Respond with the specified user's score
    @commands.command(name="score", help="List a user's +- score.")
    async def score(self, ctx, member: typing.Optional[discord.Member]):
        member = ctx.message.author if member is None else member
        # Initialize user's score if they don't already have one
        if member.mention not in scored_members:
            score_func("init", member.mention, 0)
        print(member.display_name + ' is at a ' + str(score_func("get", member.mention, None)))
        await ctx.send(member.display_name + ' is at a ' + str(score_func("get", member.mention, None)))

    # Show a scoreboard from highest to lowest for all users with a score
    @commands.command(name="scoreboard", help="Scoreboard of the highest and lowest scores.")
    async def scoreboard(self, ctx):
        # Initialize scoreboard embed message and embed description
        embed = discord.Embed(title="Scoreboard")
        desc = ""
        score_list = shelve.open("plusMinus")
        # Sort the current user scores from highest to lowest
        score_sorted = sorted(score_list.items(), key=lambda x: x[1])
        # Iterate through the scores and build the embed content
        for score in score_sorted:
            # Here "score" is a tuple, containing the user and score, adding each to a new line
            desc = str(score[0]) + ": " + str(score[1]) + "\n" + desc
        score_list.close()
        # Add some flavor text and send the message
        embed.description = "Here's the current scoreboard. Honestly can't believe these numbers: \n\n" + desc
        embed.set_footer(text="Be sure to use bb:+ and bb:- to keep our scoreboard up to date.")
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
