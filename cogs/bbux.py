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

# Library of available prizes
PRIZES = {"Seagull": [discord.Embed(title="Seagull",
                                    description="Flying coast rat.",
                                    color=common),
                      "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg/1200px-Larus_occidentalis_%28Western_Gull%29%2C_Point_Lobos%2C_CA%2C_US_-_May_2013.jpg",
                      "50",
                      "Common"],
          "Will's Shoes": [discord.Embed(title="Will's Shoes",
                                         description="They're worth so little because he owns so many.",
                                         color=common),
                           "http://www.fantastischekinderdisco.be/clown_shoes.png",
                           "2",
                           "Common"],
          "Coconut": [discord.Embed(title="Coconut",
                                    description="It's a coconut. The coconut is the proud owner of both hair and milk, "
                                                "which qualifies it as a mammal. Deadly when falling from its tropical "
                                                "treetop abode, the coconut also demonstrates the killer instinct "
                                                "necessary for survival in the animal kingdom. This may be your prize "
                                                "but make no mistake, you do not own the coconut. "
                                                "Nobody should dare to try.",
                                    color=peculiar),
                      "https://d3cizcpymoenau.cloudfront.net/images/28285/SIL_CoconutProducts_Cracked_05.png",
                      "200",
                      "Peculiar"],
          "Elliott's Gamer Chair": [discord.Embed(title="Elliott's Gamer Chair",
                                                  description="A throne for a true king. This vessel will support you "
                                                              "through gaming sessions upwards of 17 hours at a time. "
                                                              "That familiar comforting scent is sure to put you at "
                                                              "ease and allow your mind to focus solely on the task at "
                                                              "hand: bideo gaem.",
                                                  color=peculiar),
                                    "https://lh3.googleusercontent.com/-VgWN4JntMXE/VWUN1dANdkI/AAAAAAAAHpc/1gZrYKR2Sv4/s640/blogger-image-271844959.jpg",
                                    "500",
                                    "Peculiar"],
          "Lava Lamp": [discord.Embed(title="Lava Lamp",
                                      description="Hot goo in a funky tube. No ticket prize shelf or psychedelic "
                                                  "bachelor pad is complete without one. Enter a magical trance and "
                                                  "watch those enchanting blobs bounce about. Be warned, however. Do "
                                                  "not attempt to include one of these in your carry-on baggage when "
                                                  "using commercial air travel. An RPG-shaped object full of liquid "
                                                  "that sets off the x-ray machine is something best left to your "
                                                  "checked bag and not to be prodded by a TSA agent in front of you.",
                                      color=perplexing),
                        "https://www.lavalamp.com/wp-content/uploads/2017/07/2700.png",
                        "5000",
                        "Perplexing"],
          # TODO: Add "bonus stats" like, +4 Mcdonald's craving
          "Juniel's Beard Clippings": [discord.Embed(title="Juniel's Beard Clippings",
                                                     description="He can grow this easily, the blueberries not so "
                                                                 "much. Those lucky enough to brustle this beard are "
                                                                 "considered his truest friends.",
                                                     color=perplexing),
                                       "https://scottburns.files.wordpress.com/2011/12/img_0424.jpg",
                                       "7220",
                                       "Perplexing"],
          "Chuy's Gift Card": [discord.Embed(title="Chuy's Gift Card",
                                             description="A blessed meal at no cost to you. Fajitas, burritos, "
                                                         "flautas, and of course a bowl of hot queso. All of this and "
                                                         "more could be yours. Dine at the Chihuahua Bar and feel "
                                                         "those fantastic Mexican calories engorge your very soul.",
                                             color=mystifying),
                               "https://nypizzahollywood.com/wp-content/uploads/2018/11/chuys-gift-card-1.png",
                               "60000",
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
                        "200000",
                        "Fantasmaglorical"]
          }

# Open the bbux bank for reference in commands
plusMinus = shelve.open('plusMinus')  # stores the +- scores


def bank(action, member, amount):
    bbux_bank = shelve.open("bbux_bank")
    if action == "add":
        bbux_bank[member] += amount
        return bbux_bank[member]
    elif action == "retrieve":
        return bbux_bank[member]
    elif action == "remove":
        bbux_bank[member] -= amount
        return bbux_bank[member]
    bbux_bank.close()


class BBux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Just a test command to show off the form of a prize embed
    '''
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
    '''

    # Displays the information regarding a specified prize, or random one if no input is given
    @commands.command(name="prize", help="See the details on a special BBux prize!")
    async def prize(self, ctx, *, item: typing.Optional[str]):
        # Assign a random prize to display if a specific was not asked for
        item = random.choice(list(PRIZES.keys())) if item is None else item
        # Build the embed using the values from the list in the value of the key of the prize name
        embed = PRIZES[item][0]
        embed.set_image(url=PRIZES[item][1])
        embed.add_field(name="Value", value=PRIZES[item][2] + " ᘋ")
        embed.add_field(name="Quality", value=PRIZES[item][3])
        embed.set_footer(text="\"B·Bux: The fun way to waste time!\"")
        await ctx.send(embed=embed)
        # The fields need to be cleared each time a prize is displayed or the command adds another set of the same
        # embed fields for some reason.
        embed.clear_fields()

    # Tell a user what their current supply of BBux is
    @commands.command(name="bbux", help="Check your current BBux balance.")
    async def bbux(self, ctx):
        # Load the user's balance
        print(ctx.message.author.mention)
        await ctx.send(ctx.message.author.name + ", you have {0} ᘋ in your account."
                       .format(str(bank("retrieve", ctx.message.author.mention, None))))

    @commands.cooldown(rate=3, per=60 * 5, type=commands.BucketType.member)
    @commands.command(name="skeeball", help="Play a game of Skee-Ball and win some BBux.")
    async def skeeball(self, ctx):
        # Generate the skee-ball score. Nine balls are "thrown" and points are weighted to simulate accuracy.
        skee_score = sum(random.choices([10, 20, 30, 40, 50, 100], weights=(30, 40, 25, 20, 10, 5), k=9))
        # Navigate edge cases that the lambda is not designed well for
        # Score simulation showed: min. around 100, max. around 650, avg. around 250
        if skee_score < 150:
            bbux_won = 100
        elif skee_score > 450:
            bbux_won = 4000
        else:
            # Calculate prize output according to a cubic function I designed that is based on score simulations I ran
            skee_prize = lambda x: 0.0004 * pow((x - 252), 3) + 300
            bbux_won = int(skee_prize(skee_score))
        # Call the bank to adjust balance
        bank("add", ctx.message.author.mention, bbux_won)
        await ctx.send("You scored {0} on Billager's Big Baller Skee-Ball machine! You've earned {1} ᘋ."
                       .format(skee_score, bbux_won))

    '''
    # Award users with some BBux every time they use a Billager Bot command
    # TODO: See if there is some way of excluding certain commands from invoking this
    @commands.Cog.listener()
    async def on_command(self, ctx):
        # Give every user a starting balance of 20 BBux to start
        if ctx.message.author.mention not in list(bbux_bank.keys()):
            bbux_bank[str(ctx.message.author.id)] = 20
        # Initialize the user's score if they don't already have one
        if ctx.message.author.mention not in list(plusMinus.keys()):
            plusMinus[ctx.message.author.mention] = 0
        # Adjust the BBux given based on user score
        # Higher score means more BBux, reward good behavior, balancing TBD
        if plusMinus[ctx.message.author.mention] > 2:
            bbux_bank[str(ctx.message.author.id)] += 12
        else:
            bbux_bank[str(ctx.message.author.id)] += 10
    '''

    @skeeball.error
    async def skeeball_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("That's enough Skee-ball for a while! Try another game or wait a few minutes.")


def setup(bot):
    bot.add_cog(BBux(bot))
