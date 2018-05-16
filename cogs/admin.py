import discord
from discord.ext import commands

from checks import *

class Administration:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return is_admin(ctx.author)

def setup(bot):
    bot.add_cog(Administration(bot))
