import discord
from discord.ext import commands
import duckduckgo as ddg

class Internet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def (self, ctx):
        """"""

def setup(bot):
    bot.add_cog(Internet(bot))
