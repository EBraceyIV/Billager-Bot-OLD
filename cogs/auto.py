from discord.ext import commands
import random


class Auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        # Reply to the secret word with 1/100 chance
        if 'hog' in message.clean_content.lower():
            if 1 == random.randint(1, 100):
                await message.channel.send('HYPEROMEGAHOGGERS')


def setup(bot):
    bot.add_cog(Auto(bot))
