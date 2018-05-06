import discord
from discord.ext import commands

# FMS -> bot owner
# admin -> manage guild permission
# moderator -> manage messages permission

def is_FMS():
    async def pred(ctx):
        return ctx.author.id == 305289547430756354
    return commands.check(pred)

def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})
    return commands.check(pred)

def is_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_messages': True})
    return commands.check(pred)
