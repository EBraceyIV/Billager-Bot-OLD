import os
import discord
from discord.ext import commands
import TOKEN
import shelve

# TOKEN retrieved from a separate file with just a function that returns the string
TOKEN = TOKEN.token()

bot = commands.Bot(command_prefix=['bb:', 'BB:', 'Bb:', 'Bb:'],
                   description="Your very good friend, the Billager.",
                   case_insensitive=True)


# Conduct on startup
@bot.event
async def on_ready():
    print('Billager has logged in as {0}.'.format(bot.user.name))

    # Initialize BBux bank and user prize collections
    bbux_bank = shelve.open("bbux_bank")
    member_collections = shelve.open("member_collection")
    for guild in bot.guilds:
        for member in guild.members:
            if member.mention not in bbux_bank:
                bbux_bank[member.mention] = 0
            if member.mention not in member_collections:
                member_collections[member.mention] = {}
    bbux_bank.close()
    member_collections.close()

    # Load each cog included in the "cogs" directory
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):  # Safety check to not process any non-cog files
            try:
                bot.load_extension(f'cogs.{cog[:-3]}')
            except Exception as e:  # Report any cog loading errors to the console
                print("Couldn't load cog \"{0}\"".format(cog))
                print("Error: {0}".format(e))
    # Breathe a bit of life into our creation with some fun activity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with his axe."))


# This is currently just for my own reference in the future
'''
@bot.command(name='emotes', help='Dev only, does nothing (that you can see).')
async def emotes(ctx):
    emote_library = {}
    # all emotes in the guild
    for emote in ctx.guild.emojis:
        emote_library[emote.name] = emote
    print(emote_library['Drink'])
    # Display id of specific channel
    #ct = discord.utils.get(ctx.guild.text_channels, name="command-terminal")
    #print(ct.id)
'''

if __name__ == '__main__':
    bot.run(TOKEN)
