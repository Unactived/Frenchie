import discord
from discord.ext import commands

# FMS -> bot owner
# admin -> manage guild permission
# moderator -> manage messages permission

async def check_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())

def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})
    return commands.check(pred)

def is_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_messages': True})
    return commands.check(pred)
