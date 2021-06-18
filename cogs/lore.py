import discord
from discord.ext import commands
import random
import typing
import shelve
import asyncio
import datetime

# lore_keeper stores all of the discord.Embed objects for read/write
lore_list = shelve.open("loreKeeper")
all_lore = list(lore_list.keys())
lore_list.close()


# Lore management function
#   action: Add to or remove from lore record, or retrieve a lore entry to alter/display
#   member: Which lore entry to manage
#   embed: The discord.Embed content for the designated lore entry
def lore_access(action, lore_title_, embed_):
    global all_lore
    lore_keeper = shelve.open("loreKeeper")
    if action == "add":
        lore_keeper[lore_title_] = embed_
    elif action == "remove":
        del lore_keeper[lore_title_]
    elif action == "edit":
        lore_access("remove", lore_title_, None)
        lore_access("add", lore_title_, embed_)
    elif action == "retrieve":
        embed = lore_keeper[lore_title_]
        return embed
    all_lore = list(lore_keeper.keys())
    lore_keeper.close()


# Embed constructor to clear up code
#   lore_title: The name of the lore entry
#   lore_desc: The description / content of the lore entry
def embed_init(lore_title, lore_desc):
    # embed is the object that contains all the lore info, can be edited easily as an object
    embed = discord.Embed(title=lore_title,
                          description=lore_desc,
                          color=0x7289da)
    # Generate date the lore was added to add to footer
    date = datetime.date.today()
    # A randomly chosen number is given to the lore entry for show on construction
    embed.set_author(name="Lore Nugget #" + str(random.randint(1000, 9999)))
    embed.set_footer(text="Lore added: " + str(date) + "\n"
                          "More Lore? Tell BBot what needs to be remembered.")
    return embed


class Lore(commands.Cog):
    # Lore commands always take the title of the lore first

    def __init__(self, bot):
        self.bot = bot

    # Display the requested piece of lore, or a random piece if none is specified
    @commands.command(name='lore', description="View some enjoyable server lore.",
                      help="This is for lore reading.")
    async def lore(self, ctx, *, lore_title: typing.Optional[str]):
        lore_title = random.choice(all_lore) if lore_title is None else lore_title
        if lore_title not in all_lore:
            await ctx.send("You must be from a different timeline (or really bad at spelling) because we don't have "
                           "that lore on record.")
            return
        embed = lore_access("retrieve", lore_title, None)
        await ctx.send(embed=embed)

    # Display a list of all lore currently stored
    @commands.command(name="loreList", description="See a list of all available lore.",
                      help="This is for seeing what lore is currently on file.")
    async def lore_list(self, ctx):
        # Initialize the embed
        embed = discord.Embed(title="Billager's Lore Compository", color=0x7289da)
        embed.set_footer(text="More Lore? Tell BBot what needs to be remembered.")
        # To iterate on the description for the embed, start as a normal string
        description = "Here you can see the full archive of all lore currently on record.\n" \
                      "Use `bb:lore <lore title>` to read more about any entry.\n\n" \
                      "------------------------------\n\n"
        # Then add each lore by title to the description
        for lore_title in all_lore:
            description = description + "> " + lore_title + "\n"
        embed.description = description
        await ctx.send(embed=embed)

    # Add a new piece of lore to the records
    @commands.command(name="addLore", help="Add a new piece of lore to the records. Title and then description.",
                      description="Title that contain a space must be put in quotation marks. Anything after that will "
                                  "be used as the description of the lore.")
    async def add_lore(self, ctx, lore_title: str, *, lore_description: str):
        # Pass the relevant info to the embed builder
        embed = embed_init(lore_title, lore_description)
        # The lore is stored as the type embed in the shelf file
        lore_access("add", lore_title, embed)
        await ctx.send(embed=embed)

    # Edit an existing piece of lore
    @commands.command(name="editLore",
                      help="Edit a piece of lore on the records. Lore title, what's changing, then the change.")
    async def edit_lore(self, ctx, lore_title: str, edit_field: str, *, edit: str):
        if lore_title not in all_lore:
            await ctx.send("Can't find that lore!")
            return
        # Load the embed object once we know it exists so it can be edited
        embed = lore_access("retrieve", lore_title, None)
        # Lower the name of the field to edit for robustness
        if edit_field.lower() == "title":
            # Assign the edited embed to a new entry in lore_list and remove the old one
            # Easiest way I could conjure of replacing the key of a shelve entry
            embed.title = edit
            lore_access("remove", lore_title, None)
            lore_access("add", edit, embed)
        elif edit_field.lower() == "desc":
            # Reassign the description and reassign the value to the key
            embed.description = edit
            lore_access("edit", lore_title, embed)
        elif edit_field.lower() == "num":
            # Validate that users have entered a valid number (int or float)
            try:
                edit = int(edit)
            except ValueError:
                try:
                    edit = float(edit)
                except ValueError:
                    await ctx.send("Since my brain is a computer, it'll help if you make that a number instead.")
                    return
                else:
                    # Assign the manual ID number to the lore
                    embed.set_author(name="Lore Nugget #" + str(edit))
                    lore_access("edit", lore_title, embed)
            else:
                # Assign the manual ID number to the lore
                embed.set_author(name="Lore Nugget #" + str(edit))
                lore_access("edit", lore_title, embed)
        else:
            await ctx.send("That's not an editable field for the lore.")
            return

        await ctx.send(embed=embed)

    # Remove a piece of lore from the records
    @commands.command(name="killLore", help="Remove a piece of lore from the records.",
                      description="Only the user who issues this command can reply to confirm.")
    async def kill_lore(self, ctx, lore_title):
        # Check to see if the lore exists
        if lore_title not in all_lore:
            await ctx.send("Can't find that lore!")
            return

        # Ask for confirmation to delete the lore
        await ctx.send("Are you sure you want to destroy the " + lore_title + " lore? A simple yes or no will do.")

        # The yes/no check for the confirmation message used in wait_for below
        def check(message):
            # Only allow the user who made the request to confirm the request
            if message.content.lower() == "yes" and ctx.message.author == message.author:
                return "yes"
            elif message.content.lower() == "no" and ctx.message.author == message.author:
                return "no"
            else:
                return False

        # Process the confirmation message
        try:
            # Give the user 5 seconds to confirm according to the check function
            kill_confirm = await self.bot.wait_for('message', timeout=5.0, check=check)
        except asyncio.TimeoutError:  # Inform user they ran out of time to confirm
            await ctx.send("This is taking too long. Next time, be ready to pull the trigger.")
        else:
            # Delete the lore if confirmation check is passed
            if kill_confirm.content == "yes":
                lore_access("remove", lore_title, None)
                await ctx.send("The deed is done.")
            else:
                await ctx.send("The lore remains intact.")

    # Send a "relevant" error message if there was a problem editing lore
    @edit_lore.error
    async def edit_lore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please don't do that. Try again but try harder.")
        else:
            print(error)
            await ctx.send("You really messed something up. This could be a problem.")

    # Send a "relevant" error message if there was a problem adding lore
    @add_lore.error
    async def add_lore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please don't do that. Try again but try harder.")
        else:
            await ctx.send("You really messed something up. This could be a problem.")


def setup(bot):
    bot.add_cog(Lore(bot))
