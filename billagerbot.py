import os
import discord
from discord.ext import commands
import TOKEN

# BOT TOKEN
TOKEN = TOKEN.token()

# bot = commands.Bot(command_prefix=['bb:', 'BB:', 'Bb:', 'Bb:'], description="Your very good friend, the Billager.")
bot = commands.Bot(command_prefix=['tb:'], description="Your very good friend, the Billager.")

@bot.event
async def on_ready():
    print('Billager has logged in as {0}.'.format(bot.user.name))
    for cog in os.listdir("cogs"):
        if cog.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{cog[:-3]}')
            except Exception as e:
                print('Couldn\'t load cog \"{0}\"'.format(cog))
                print('Error: {0}'.format(e))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="his conscience"))


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


if __name__ == '__main__':
    bot.run(TOKEN)
