import discord
from discord.ext import commands
import random
import datetime
import asyncio
import shelve


class Auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check every message that comes through and perform a hog-check
    @commands.Cog.listener()
    async def on_message(self, message):
        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        # Reply to the secret word with 1/100 chance
        if 'hog' in message.clean_content.lower() and 1 == random.randint(1, 100):
            await message.channel.send('HYPEROMEGAHOGGERS')

    # Every Friday night, make a call out post about whoever got the lowest score that week
    @commands.cooldown(rate=1, per=60 * 60, type=commands.BucketType.guild)
    @commands.Cog.listener()
    async def on_message(self, message):
        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        time = datetime.datetime.now()
        if time.day == 6 and time.hour in [11, 12, 13]:
            await asyncio.sleep(5)
            plusMinus = shelve.open("plusMinus")
            # Sort the current user scores from highest to lowest
            score_sorted = sorted(plusMinus.items(), key=lambda x: x[1])
            plusMinus.close()
            await message.channel.send("This is your weekly Bad Score Callout Post, a public service brought to you by "
                                       "Billager Bot. \n"
                                       "This week, " + str(score_sorted[0][0]) + " has the worst score so far. All the "
                                       "way down at a fat " + str(score_sorted[0][1]) + "!")


def setup(bot):
    bot.add_cog(Auto(bot))
