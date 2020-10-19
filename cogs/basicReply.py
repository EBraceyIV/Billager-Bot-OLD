import discord
from discord.ext import commands
import random
from mcstatus import MinecraftServer

# Define emotes
dwayneBlock = '<:dwayneBlock:578999476824440852>'
depression = '<:depression:605507923619086349>'
billagermine = '<:billagermine:679882568740503648>'
beefBrain = '<:BeefBrain:631694337549271050>'
hellHog_RAGE = '<:hellHog_RAGE:610668471520460817>'
WillBrain = '<:WillBrain:688918968785829894>'
ZBillagerChop = '<a:ZBillagerChop:619169326829928449>'
monkaGun = '<:monkaGun:650922885627772949>'
fortCry = '<:fortCry:600190388241694770>'

# mcstatus init
server = MinecraftServer.lookup("192.99.4.195:25577")  # my minecraft server


class BasicReply(commands.Cog, name="Basic Replies"):
    def __init__(self, bot):
        self.bot = bot

    # This currently serves no real purpose. Just learning the channels and utils functionality.
    @commands.command(name='channels', help='Dev only, does nothing (that you can see).', hidden=True)
    async def channels(self, ctx):
        # All channels in the guild
        for channel in ctx.guild.channels:
            print(channel)
        # Display id of specific channel, given the name in the guild
        ct = discord.utils.get(ctx.guild.text_channels, name="command-terminal")
        print(str(ct.id) + ' ' + ct.name + ' ' + ct.topic)

    # An early test reply command with an Animal Crossing twist
    @commands.command(name='nook', help='That two-bit Tanooki.')
    async def nook(self, ctx):
        response = "I will send Kicks to break Tom Nook's kneecaps."
        await ctx.send(response)

    # Basic send a message command
    @commands.command(name='watch', help='He likes to watch.')
    async def watch(self, ctx):
        response = 'I like to watch.'
        await ctx.send(response)

    # Randomly picks a Will-thing to say
    @commands.command(name='will', aliases=['Will'], help='Will Simulator',
                      description="Billager's many impressions of Will, he's got more than 30!")
    async def will(self, ctx):
        willReplies = ["pepehands " + depression,
                       "oh yeah?",
                       "die in a fire " + hellHog_RAGE,
                       "smile",
                       "i've got a galaxy brain idea " + WillBrain,
                       "**NO ANIME** " + ZBillagerChop,
                       "?????????????",
                       "oh, i see",
                       "you know what? i'll take it",
                       "and **LIE**",
                       "c!play surf rock anthology volume 1",
                       "c!play sounds of the supermarket",
                       "c!play a girl worth fighting for",
                       monkaGun,
                       "GET IN THE CAR HORATIO",
                       "I can't believe this",
                       "you wanna win",
                       "i'm so tired bro",
                       "secretly i'm vulnerable and that's why i'm aggressive " + fortCry,
                       "Please bro",
                       "I went to Wendy’s",
                       "I went to Steak & Shake",
                       "PLEASE",
                       "And uh",
                       "*one of those wacky purple emotes*",
                       "YES",
                       "HOG",
                       "it's time to end this",
                       "Never say that to me ever again",
                       "Gachi",
                       "NICE BOAT",
                       "I bought more shoes",
                       "Dunston checks in",
                       "I cannot believe you",
                       "I will remember this",
                       "I don't remember the touch of a woman " + fortCry]
        response = random.choice(willReplies)
        await ctx.send(response)

    # Basic reply using an emote id
    @commands.command(name="dwayne", help='Dwayne himself')
    async def block(self, ctx):
        response = '<:dwayneBlock:578999476824440852>'
        await ctx.send(response)

    # Provides current player count and latency to the Minecraft server
    @commands.command(name="blocks", help='Minecraft Server Info')
    async def blocks(self, ctx):
        # Get all of the server information
        status = server.status()

        # Build the embed message using the server query
        embed = discord.Embed(title='Dwayneblock Memorial Minecraft Server',
                              color=0xdd3333,
                              description='{0} Come play with blocks at {1}:{2}'
                              .format(dwayneBlock, server.host, server.port))
        embed.add_field(name='Players Online:', value=status.players.online)
        embed.add_field(name='Latency:', value=str(status.latency) + ' ms')
        embed.add_field(name='Game Version:', value=status.version.name)
        embed.set_footer(text='This server is hosted out of Houston, TX by Villagerhost.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BasicReply(bot))
