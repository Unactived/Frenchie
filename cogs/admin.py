import discord
from discord.ext import commands

class Administration:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Administration(bot))
