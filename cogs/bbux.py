import discord
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


class bbux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prize')
    async def prize(self, ctx):
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


def setup(bot):
    bot.add_cog(bbux(bot))
