import discord
from discord.ext import commands
import random
import shelve
import asyncio

# lore_keeper stores all of the discord.Embed objects for read/write
lore_keeper = shelve.open('loreKeeper')
all_lore = list(lore_keeper.keys())


# Embed constructor to clear up code
def embed_init(lore_title, lore_desc, lore_num):
    # embed is the object that contains all the lore info, can be edited easy due to modularity
    embed = discord.Embed(title=lore_title,
                          description=lore_desc,
                          color=0x7289da)
    # embed.author is constructed this way to allow generation of the number separately from the flavor text
    embed.set_author(name='Lore Nugget #' + lore_num)
    embed.set_footer(text='More Lore? Tell BBot what needs to be remembered.')
    return embed


class Lore(commands.Cog):
    # Lore commands always take the title of the lore first

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lore', description="View some enjoyable server lore.",
                      help="This is for lore reading.", aliases=['Lore'])
    async def lore(self, ctx, *, lore_title):
        embed = lore_keeper[lore_title]
        await ctx.send(embed=embed)

    @commands.command(name='addLore', aliases=['AddLore'])
    async def addLore(self, ctx, lore_title: str, *, lore_description: str):
        lore_num = str(random.randint(1000, 9999))
        embed = embed_init(lore_title, lore_description, lore_num)
        lore_keeper[lore_title] = embed
        await ctx.send(embed=embed)

    @commands.command(name='editLore', aliases=['EditLore'])
    async def editLore(self, ctx, lore_title: str, edit_field: str, *, edit: str):
        if lore_title not in lore_keeper:
            await ctx.send('Can\'t find that lore!')
            return

        # Load the embed object once we know it exists so it can be edited
        embed = lore_keeper[lore_title]
        # Lower the name of the field to edit for robustness
        if edit_field.lower() == "title":
            # Assign the edited embed to a new entry in lore_keeper and remove the old one
            # Easiest way I could conjure of replacing the key of a shelve entry
            embed.title = edit
            lore_keeper[edit] = embed
            del lore_keeper[lore_title]
        elif edit_field.lower() == "desc":
            # Reassign the description and reassign the value to the key
            embed.description = edit
            lore_keeper[lore_title] = embed
        else:
            await ctx.send('That\'s not an editable field for the lore.')
            return

        await ctx.send(embed=embed)

    @commands.command(name="killLore", aliases=['KillLore'],
                      help="Remove a piece of lore from the records.",
                      description="Only the user who issues this command can reply to confirm.")
    async def killLore(self, ctx, lore_title):
        if lore_title not in lore_keeper:
            await ctx.send('Can\'t find that lore!')
            return
        await ctx.send("Are you sure you want to destroy the " + lore_title + " lore? A simple yes or no will do.")

        def check(message):
            if message.content.lower() == "yes" and ctx.message.author == message.author:
                return "yes"
            elif message.content.lower() == "no" and ctx.message.author == message.author:
                return "no"
            else:
                return False

        try:
            kill_confirm = await self.bot.wait_for('message', timeout=5.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("This is taking too long. Next time, be ready to pull the trigger.")
        else:
            if kill_confirm.content == "yes":
                del lore_keeper[lore_title]
                await ctx.send("The deed is done.")
            else:
                await ctx.send("The lore remains intact.")

    @lore.error
    async def lore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            lore_title = random.choice(all_lore)
            embed = lore_keeper[lore_title]
            await ctx.send(embed=embed)
        else:
            await ctx.send("You really messed something up. This could be a problem.")

    @editLore.error
    async def editLore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please don't do that. Try again but try harder.")
        else:
            await ctx.send("You really messed something up. This could be a problem.")

    @addLore.error
    async def addLore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please don't do that. Try again but try harder.")
        else:
            await ctx.send("You really messed something up. This could be a problem.")


def setup(bot):
    bot.add_cog(Lore(bot))
