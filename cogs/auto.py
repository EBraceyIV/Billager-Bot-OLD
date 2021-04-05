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
        # Global variable to keep track of whether or not the callout post has been made yet out of the scope of this
        # listener so that it does not trigger multiple times
        global called_out

        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        # The day and hour of the message being sent is needed to trigger the callout post
        time = datetime.datetime.now()
        if not called_out:
            # Automatically know if I'm using the test bot or if Billager Bot is in control
            # FOR TESTING: 720833461329461347  |  FOR USE: 743616007435976754
            callout_channel = 720833461329461347 if self.bot.user.name == "BotTest" else 743616007435976754

            # The callout post can be triggered on Fridays between 5 and 7 P.M. EST in a specific channel
            if time.weekday() == 4 and time.hour in [17, 18, 19] and message.channel.id == callout_channel:
                # Wait a short while after detecting a valid trigger message to make it seem more organic, but only
                # after setting called_out to True so that no other messages trigger another post during the wait
                called_out = True
                print("Callout post inbound.")
                await asyncio.sleep(120)

                # Sort the current user scores from highest to lowest
                plus_minus = shelve.open("plusMinus")
                score_sorted = sorted(plus_minus.items(), key=lambda x: x[1])
                plus_minus.close()

                # Send our fun little message letting our friend know they should try making better jokes
                await message.channel.send("This is your weekly Bad Score Callout Post, a public service brought to "
                                           "you by Billager Bot. \n"
                                           "This week, " + str(score_sorted[0][0]) + " has the worst score so far. "
                                           "All the way down at a fat " + str(score_sorted[0][1]) + "!")
        else:
            # Reset the called_out status on Saturday
            if called_out and time.weekday() == 5:
                called_out = False
                # Reset the whole scoreboard monthly, this should typically catch the last Saturday of the month
                if time.day >= 24:
                    plus_minus = shelve.open("plusMinus")
                    plus_minus.clear()
                    plus_minus.close()


def setup(bot):
    bot.add_cog(Auto(bot))
