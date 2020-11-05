import discord
from discord.ext import commands
import random
import datetime
import asyncio
import shelve

called_out = False


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
    @commands.Cog.listener()
    async def on_message(self, message):
        global called_out

        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        time = datetime.datetime.now()
        if not called_out:
            if time.day == 6 and time.hour in [17, 18, 19] and message.channel.id == 743616007435976754:
                called_out = True
                await asyncio.sleep(5)
                plusMinus = shelve.open("plusMinus")
                # Sort the current user scores from highest to lowest
                score_sorted = sorted(plusMinus.items(), key=lambda x: x[1])
                plusMinus.close()
                await message.channel.send("This is your weekly Bad Score Callout Post, a public service brought to you by "
                                           "Billager Bot. \n"
                                           "This week, " + str(score_sorted[0][0]) + " has the worst score so far. All the "
                                           "way down at a fat " + str(score_sorted[0][1]) + "!")
        else:
            if called_out and time.day == 5:
                called_out = False



def setup(bot):
    bot.add_cog(Auto(bot))
