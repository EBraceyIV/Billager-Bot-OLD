import discord
import typing
import random
import shelve
from discord.ext import commands

# B·Bux is the specialized Billager prize ticket system
# I have no idea what this is really meant to be but I'd gonna do it anyway
# Deciding on a symbol, currently between these: ᘋ, ᛒ, ᴃ

# Rarity colors:
common = 0x150549
peculiar = 0xff22df
perplexing = 0xf0ff00
mystifying = 0xff4d00
fantasmaglorical = 0x00ecff

PRIZES = {"Seagull": [discord.Embed(title="Seagull",
                                    description="Flying coast rat.",
                                    color=common),
                      "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg/1200px-Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg",
                      "50 ᘋ",
                      "Common"],
          "Will's Shoes": [discord.Embed(title="Will's Shoes",
                                         description="They're worth so little because he owns so many.",
                                         color=common),
                           "http://www.fantastischekinderdisco.be/clown_shoes.png",
                           "2 ᘋ",
                           "Common"],
          "Coconut": [discord.Embed(title="Coconut",
                                    description="It's a coconut. The coconut is the proud owner of both hair and milk, "
                                          "which qualifies it as a mammal. Deadly when falling from its tropical "
                                          "treetop abode, the coconut also demonstrates the killer instinct necessary "
                                          "for survival in the animal kingdom. This may be your prize but make no "
                                          "mistake, you do not own the coconut. Nobody should dare to try.",
                                    color=peculiar),
                      "https://d3cizcpymoenau.cloudfront.net/images/28285/SIL_CoconutProducts_Cracked_05.png",
                      "200 ᘋ",
                      "Peculiar"],
          "Lava Lamp": [discord.Embed(title="Lava Lamp",
                                      description="Hot goo in a funky tube. No ticket prize shelf or psychedelic "
                                                  "bachelor pad is complete without one. Enter a magical trance and "
                                                  "watch those enchanting blobs bounce about. Be warned, however. Do "
                                                  "not attempt to include one of these in your carry-on baggage when "
                                                  "using commercial air travel. An RPG-shaped object full of liquid "
                                                  "that sets off the x-ray machine is something best left to your "
                                                  "checked bag and not to be prodded by a TSA agent in front of you."),
                        "https://www.lavalamp.com/wp-content/uploads/2017/07/2700.png",
                        "5000 ᘋ",
                        "Perplexing"],
          "Chuy's Gift Card": [discord.Embed(title="Chuy's Gift Card",
                                             description="A blessed meal at no cost to you. Fajitas, burritos, "
                                                         "flautas, and of course a bowl of hot queso. All of this and "
                                                         "more could be yours. Dine at the Chihuahua Bar and feel "
                                                         "those fantastic Mexican calories engorge your very soul.",
                                             color=mystifying),
                               "https://nypizzahollywood.com/wp-content/uploads/2018/11/chuys-gift-card-1.png",
                               "60000 ᘋ",
                               "Mystifying"],
          "Dan's Car": [discord.Embed(title="Dan's Car",
                                      description="Like a father and his son, Dan built this mean machine with his own "
                                                  "two hands in his garage. This spicy vroomer has unlimited vehicular "
                                                  "potential. A whole engine, all the tires, seats, a full tank of "
                                                  "headlight fluid, and legal dispensation to drive an extra 3 miles "
                                                  "per hour in any school zone. The open road beckons, will you answer "
                                                  "the call?",
                                      color=fantasmaglorical),
                        "https://vignette3.wikia.nocookie.net/deathbattlefanon/images/a/a8/DC_Comics_-_The_Batmobile_1960s_era.png/revision/latest?cb=20160527111804",
                        "200000 ᘋ",
                        "Fantasmaglorical"]
          }

bbux_bank = shelve.open("bbux_bank")
pmFile = shelve.open('plusMinus') #stores the +- scores

class bbux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Just a test command to show off the form of a prize embed
    @commands.command(name='coconut')
    async def coconut(self, ctx):
        embed = discord.Embed(title="Coconut",
                              description="It's a coconut. The coconut is the proud owner of both hair and milk, "
                                          "which qualifies it as a mammal. Deadly when falling from it's tropical "
                                          "treetop abode, the coconut also demonstrates the killer instinct necessary "
                                          "for survival in the animal kingdom. This may be your prize but make no "
                                          "mistake, you do not own the coconut. Nobody should dare to try.",
                              color=peculiar)
        embed.set_image(url="https://d3cizcpymoenau.cloudfront.net/images/28285/SIL_CoconutProducts_Cracked_05.png")
        embed.add_field(name="Value", value="200 ᘋ")
        embed.add_field(name="Quality", value="Peculiar")
        embed.set_footer(text="\"B·Bux: The fun way to waste time!\"")
        await ctx.send(embed=embed)

    # Displays the information regarding a specified prize, or random one if no input is given
    @commands.command(name="prize")
    async def prize(self, ctx, *, item: typing.Optional[str] = None):
        # Assign a random prize to display if a specific was not asked for
        if item is None:
            item = random.choice(list(PRIZES.keys()))
        # Build the embed using the values from the list in the value of the key of the prize name
        embed = PRIZES[item][0]
        embed.set_image(url=PRIZES[item][1])
        embed.add_field(name="Value", value=PRIZES[item][2])
        embed.add_field(name="Quality", value=PRIZES[item][3])
        embed.set_footer(text="\"B·Bux: The fun way to waste time!\"")
        await ctx.send(embed=embed)
        # The fields need to be cleared or each time a prize is displayed it adds another set of the same fields for
        # some reason.
        embed.clear_fields()

    @commands.command(name="bbux")
    async def bbux(self, ctx):
        await ctx.send(str(ctx.message.author.name) + ", you have " + str(bbux_bank[ctx.message.author.mention]) +
                       " ᘋ in your account.")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.message.author.mention not in list(bbux_bank.keys()):
            bbux_bank[ctx.message.author.mention] = 20
        if ctx.message.author.mention not in list(pmFile.keys()):
            pmFile[ctx.message.author.mention] = 0
        if pmFile[ctx.message.author.mention] > 2:
            bbux_bank[ctx.message.author.mention] += 12
        else:
            bbux_bank[ctx.message.author.mention] += 10


def setup(bot):
    bot.add_cog(bbux(bot))
