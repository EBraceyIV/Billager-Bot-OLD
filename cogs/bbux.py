import discord
import typing
import random
import shelve
from discord.ext import commands
import prizes
import re

# B·Bux is the specialized Billager prize ticket system
# Represented by this symbol: ᘋ
# I chose it at random from the Unicode compendium for it's vague resemblance of the letter B

# Rarity colors:
common = 0x150549
peculiar = 0xff22df
perplexing = 0xf0ff00
mystifying = 0xff4d00
fantasmaglorical = 0x00ecff

# Library of available prizes
PRIZES = prizes.prizes()


# BBux Bank management function
#   action: Add or remove to a balance, or see what the current balance is
#   member: Which user's balance to manage
#   amount: How many BBux to add/remove
def bank(action, member, amount):
    bbux_bank = shelve.open("bbux_bank")
    if action == "add":
        bbux_bank[member] += amount
        return bbux_bank[member]
    elif action == "retrieve":
        return bbux_bank[member]
    elif action == "remove":
        bbux_bank[member] -= int(amount)
        return bbux_bank[member]
    bbux_bank.close()


# BBux prize management function
#   add: Adds the designated prize to the user's collection
#   remove: Removes the designated prize to the user's collection
#   retrieve: Returns the the prizes owned by the user
def collection(action, member, prize):
    # Making changes using update() here only works when using a temporary dict to update the value, apparently
    member_collections = shelve.open("member_collection")

    # Handle adding a new or duplicate prize to a user's collection
    if action == "add":
        # Handle adding duplicates first, other wise add as new prize
        if prize in list(member_collections[member].keys()):
            temp = member_collections[member]
            temp.update({prize: member_collections[member][prize] + 1})
            member_collections[member] = temp
        else:
            temp = member_collections[member]
            temp.update({prize: 1})
            member_collections[member] = temp
        return
    elif action == "remove":
        # Remove a single prize from a user's collection if they own multiple of that prize
        if member_collections[member][prize] > 1:
            temp = member_collections[member]
            temp.update({prize: member_collections[member][prize] - 1})
            member_collections[member] = temp
        # Removing the only one of a prize removes it's key from the collection dict
        else:
            temp = member_collections[member]
            del temp[prize]
            member_collections[member] = temp
        return
    # Return all prizes in a user's collection
    elif action == "retrieve":
        return member_collections[member]
    member_collections.close()


class BBux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Displays a list of the available prizes
    @commands.command(name="myPrizes", help="See a list of everything in your prize collection!")
    async def prizes(self, ctx):
        user_prizes = collection("retrieve", ctx.message.author.mention, None)
        embed = discord.Embed(title=ctx.message.author.display_name + "'s Prizes", color=ctx.message.author.color)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        for prize in user_prizes.keys():
            embed.add_field(name=prize, value="You own " + str(user_prizes[prize]) + ".")
        await ctx.send(embed=embed)

    # Displays the information regarding a specified prize, a list of all prizes, or a random prize if no input is given
    @commands.command(name="prize", help="See the details on a special BBux prize!")
    async def prize(self, ctx, *, item: typing.Optional[str]):
        if item is not None:
            # Format item so that ’ and ' don't get caught up in the PRIZES keys, also make case insensitive
            item = re.sub(r"[’']", "", item.lower())
        else:
            # Assign a random prize to display if a specific was not asked for
            item = random.choice(list(PRIZES.keys())) if item is None else item

        # Display full prize list
        if item == "all":
            prize_names = list(PRIZES.keys())
            embed = discord.Embed(title="Prize Shelf",
                                  description="Come one, come all. "
                                              "See the bounty that awaits you on B. Bot's prize shelf!",
                                  color=0xfffffe)
            # Generate the prize shelf and sort by rarity / value
            for rarity in prizes.rarities:
                embed.add_field(name="**" + rarity + "s**",
                                value="__Valued at " + prizes.values[prizes.rarities.index(rarity)] + "__",
                                inline=False)
                for prize in prize_names:
                    if PRIZES[prize][3] == rarity:
                        embed.add_field(name=PRIZES[prize][0].title, value=PRIZES[prize][2] + " ᘋ", inline=True)

            await ctx.send(embed=embed)
            return

        # Check that the requested item exists
        if item not in list(PRIZES.keys()):
            print(item)
            await ctx.send("That prize does not exist, much like my interest in your nonsensical request.")
            return
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
    async def bbux(self, ctx, action: typing.Optional[str], *, prize: typing.Optional[str]):
        if prize is not None:
            # Format item so that ’ and ' don't get caught up in the PRIZES keys, also make case insensitive
            prize = re.sub(r"[’']", "", prize.lower())
        # Load the user's balance if no arguments are passed
        if action is None:
            await ctx.send(ctx.message.author.name + ", you have {0} ᘋ in your account."
                           .format(str(bank("retrieve", ctx.message.author.mention, None))))
        # Process a redemption request for a prize
        elif action.lower() == "buy":
            # Check if the requested prize exists
            if prize not in list(PRIZES.keys()):
                await ctx.send("That prize does not exist, much like my interest in your nonsensical request.")
                return
            # Check to see if the user has enough BBux to make the transaction
            if bank("retrieve", ctx.message.author.mention, None) < int(PRIZES[prize][2]):
                await ctx.send("You're too poor. Stop that.")
            else:
                # Conduct the transaction
                bank("remove", ctx.message.author.mention, PRIZES[prize][2])
                collection("add", ctx.message.author.mention, PRIZES[prize][0].title)
                await ctx.send("You've redeemed {0} of your BBux for this wonderful item: {1}"
                               .format(PRIZES[prize][2], PRIZES[prize][0].title) +
                               "\n" + "Congratulations on your shiny new prize!")
        # Process a sell request for a prize
        elif action.lower() == "pawn":
            # Check if the requested prize exists
            if prize not in list(PRIZES.keys()):
                await ctx.send("That prize does not exist, much like my interest in your nonsensical request.")
                return
            member_prizes = collection("retrieve", ctx.message.author.mention, PRIZES[prize][0].title)
            if PRIZES[prize][0].title not in member_prizes:
                await ctx.send("This isn't some Kickstarter, you can't sell something you don't actually have yet.")
            else:
                collection("remove", ctx.message.author.mention, PRIZES[prize][0].title)
                buy_back = random.randint(int(int(PRIZES[prize][2]) * 0.35), int(int(PRIZES[prize][2]) * 0.65))
                bank("add", ctx.message.author.mention, buy_back)
                await ctx.send("That didn't depreciate too badly, you still got back {0} ᘋ for "
                               "pawning that thing off. ".format(buy_back))
        # List users and their BBux balances
        # elif action.lower() == "list":
        #     # Sort user BBux balances
        #     desc = ""
        #     bbux_bank = shelve.open("bbux_bank")
        #     bank_sorted = sorted(bbux_bank.items(), key=lambda x: x[1])
        #     # Iterate through the balances
        #     for balance in bank_sorted:
        #         # Here "balance" is a tuple, containing the user and score, adding each to a new line
        #         desc = str(balance[0]) + ": " + str(balance[1]) + "\n" + desc
        #     print(desc)
        #     await ctx.send(desc)

        # Invalid action reply
        else:
            await ctx.send("That's not an option. You can buy or pawn.")

    # Skeeball machine to earn BBux
    @commands.cooldown(rate=3, per=60 * 5, type=commands.BucketType.member)
    @commands.command(name="skeeball", help="Play a game of Skee-Ball and win some BBux.")
    async def skeeball(self, ctx):
        # Generate the skee-ball score. Nine balls are "thrown" and points are weighted to simulate accuracy.
        skee_score = sum(random.choices([10, 20, 30, 40, 50, 100], weights=(30, 40, 25, 20, 10, 5), k=9))
        # Navigate edge cases that the lambda is not designed well for
        # Score simulation showed: min. around 100, max. around 650, avg. around 250
        if skee_score <= 170:
            bbux_won = 150
        elif skee_score >= 500:
            bbux_won = 7000
        else:
            # Calculate prize output according to a cubic function I designed that is based on score simulations I ran
            skee_prize = lambda x: 0.0004 * pow((x - 252), 3) + 300
            bbux_won = int(skee_prize(skee_score))
        # Call the bank to adjust balance
        bank("add", ctx.message.author.mention, bbux_won)
        await ctx.send("You scored {0} on Billager's Big Baller Skee-Ball machine! You've earned {1} ᘋ."
                       .format(skee_score, bbux_won))

    # Slot machine to earn BBux
    @commands.cooldown(rate=10, per=60 * 10, type=commands.BucketType.member)
    @commands.command(name="slots", help="Play a round on the slot machine and win some BBux.",
                      description="Play one of Billager's fantastical slot machines. Default bet is 100, or put as "
                                  "much of your money where your mouth is as you'd like.")
    async def slots(self, ctx, bet: typing.Optional[int] = 100):
        # Check that user has enough BBux to place their bet
        if bank("retrieve", ctx.message.author.mention, None) < 100:
            await ctx.send("The default bet is only 100 ᘋ and you don't even have that much? Try the skeeball machine.")
            return
        elif bank("retrieve", ctx.message.author.mention, None) < bet:
            await ctx.send("You don't have enough BBux to make that kind of bet!")
            return
        # Subtract user's bet from their balance
        bank("remove", ctx.message.author.mention, bet)

        # Function to handle two-of-a-kind matches on the slot machine
        async def double_win(slot_match):
            bbux_won = int(bet * slot_options[slot_results[slot_match]] * 1.25)
            bank("add", ctx.message.author.mention, bbux_won)
            await ctx.send("**{0} DOUBLE!** Well, at least you got two of a kind. You can have {1} ᘋ for that."
                           .format(slot_results[slot_match], bbux_won))

        # Generate a list of icons to represent the results of the slot machine, the middle 3 is a row that counts
        slot_options = {"💎": 20, "💰": 10, "💸": 5, "💵": 2, "🧾": 1, "💣": 0}
        slot_vals = random.choices(list(slot_options.keys()), weights=(5, 8, 12, 20, 35, 8), k=9)
        slot_results = slot_vals[3:6]

        # Display the results, line by line, color code the middle line
        embed_top = discord.Embed(description="{0}  --  {1}  --  {2}"
                                  .format(slot_vals[0], slot_vals[1], slot_vals[2]), color=0xfffffe)
        await ctx.send(embed=embed_top)
        embed_mid = discord.Embed(description="{0}  --  {1}  --  {2}"
                                  .format(slot_vals[3], slot_vals[4], slot_vals[5]), color=0xff6600)
        await ctx.send(embed=embed_mid)
        embed_bottom = discord.Embed(description="{0}  --  {1}  --  {2}"
                                     .format(slot_vals[6], slot_vals[7], slot_vals[8]), color=0xfffffe)
        await ctx.send(embed=embed_bottom)

        # Process results of slot roll, a bomb gives no rewards even with a double, no match gives no reward,
        # a double gives some reward, a triple gives big reward, just a diamond gives a tiny reward
        if "💣" in slot_results:
            await ctx.send("**💥 KABOOM!** That's a BOMBO! You win a big fat nothing.")
        elif slot_results[0] == slot_results[1] == slot_results[2]:
            bbux_won = bet * slot_options[slot_results[0]] * 2
            bank("add", ctx.message.author.mention, bbux_won)
            await ctx.send("**{0} CHA-CHING!** That's a full match! Enjoy your deluxe mega payout of {1} ᘋ!"
                           .format(slot_results[0], bbux_won))
        elif slot_results[0] == slot_results[1] or slot_results[0] == slot_results[2]:
            await double_win(0)
        elif slot_results[1] == slot_results[2]:
            await double_win(1)
        elif "💎" in slot_results:
            bbux_won = int(bet / 4)
            bank("add", ctx.message.author.mention, bbux_won)
            await ctx.send("💎 Diamond in the rough! I'll let you keep {0} ᘋ from your bet for finding me one of these."
                           .format(bbux_won))
        else:
            await ctx.send("**❌ WOMP WOMP!** No matches for you! Please try again. Maybe with a bigger bet...")

    @skeeball.error
    async def skeeball_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("That's enough Skee-ball for a while! Try another game or wait a few minutes.")

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Whoa buddy, that's a lot of slots. Take it easy and try something else for a little while.")


def setup(bot):
    bot.add_cog(BBux(bot))
