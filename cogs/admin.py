import discord
from discord.ext import commands

from checks import *

class Administration:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return is_admin(ctx.author)

    @commands.command()
    async def setup(self, ctx):
        """Sets guild's prefix and welcome/goodbye messages"""
        await ctx.send('Thanks for inviting me *and running this command*\
:blush:\nCurrent prefix is {self.prefix}')

def setup(bot):
    bot.add_cog(Administration(bot))
