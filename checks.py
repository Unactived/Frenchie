import discord
from discord.ext import commands

def is_FMS():
    async def predicate(ctx):
        return ctx.author.id == 305289547430756354
    return commands.check(predicate)
