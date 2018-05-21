import discord
from discord.ext import commands

from checks import *

class Administration:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        # We're in a guild and with its owner
        return ctx.guild is not None and ctx.author.id == ctx.guild.owner_id

    @commands.command(hidden=True)
    async def setup(self, ctx):
        """Sets guild's prefix and welcome/goodbye messages"""
        await ctx.send('Thanks for inviting me *and running this command*\
:blush:\nCurrent prefix is {self.prefix}')

def setup(bot):
    bot.add_cog(Administration(bot))
