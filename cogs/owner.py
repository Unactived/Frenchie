import discord
from discord.ext import commands
import traceback
import os
import sys, io
import sqlite3

from config import *
from checks import *

class Owner:
    def __init__(self, bot):
        self.bot = bot

    # Owner check
    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=['streaming', 'listening', 'watching'], hidden=True)
    async def playing(self, ctx, media=f'{prefix}info | {prefix}help'):
        """Update bot presence accordingly to invoke command"""
        # Need URL for streaming
        p_types = {'playing': 0, 'streaming':1, 'listening': 2, 'watching': 3}
        activity = discord.Activity(name=media, type=p_types[ctx.invoked_with])

        await self.bot.change_presence(activity=activity)

    @commands.command(hidden=True)
    async def guildlist(self, ctx):
        """Displays all guilds the bot is on and their members amount"""
        emb = discord.Embed(title="Frenchie's server list", color=BLUE)
        if len(self.bot.guilds) > 10: range = 10
        else: range = len(self.bot.guilds)
        for guild in self.bot.guilds[:range-1]:
            emb.add_field(name=guild.name, value=f"{guild.member_count} members")
        await ctx.send(embed=emb)

    @commands.command(hidden=True)
    async def guildinfo(self, ctx, guild: str):
        """Displays stuff on a given guild, and an invite if possible"""
        guild = discord.utils.get(self.bot.guilds, name=guild)
        emb = discord.Embed(title=f"{guild.name}", color=BLUE)
        emb.set_thumbnail(url=guild.icon_url)
        emb.add_field(name="Region",value=f'{guild.region}')
        emb.add_field(name="Members",value=guild.member_count)
        try:
            invite = await guild.text_channels[0].create_invite(unique=False)
            invite_link = f"[invite](https://discord.gg/{invite.code})"
        except Exception as e:
            invite_link = e
        emb.add_field(name="Invite",value=invite_link)

        await ctx.send(embed=emb)

    @commands.command(hidden=True)
    async def load(self, ctx, *, extension):
        """Loads a cog"""
        try:
            self.bot.load_extension(extension)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{SQUARED OK}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, extension):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(extension)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{SQUARED OK}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, extension):
        """Reloads a module."""
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{SQUARED OK}')

    @commands.command(hidden=True)
    async def kill(self, ctx):
        """Kills process"""
        await self.bot.logout()

    @commands.command(hidden=True)
    async def commit(self, ctx, branch="master"):
        """Kills process, then fetch and launch the given branch from Github"""
        await self.bot.logout()
        os.system(f'./redeploy.sh {branch}') # Reload Github and bot

    @commands.guild_only()
    @commands.command(hidden=True)
    async def say(self, ctx, channel: discord.TextChannel, *, text: str):
        """Makes the bot say something in a given current guild's channel"""
        await channel.send(text)

    @commands.is_owner()
    @commands.command(name='eval', hidden=True)
    async def _eval(self, ctx, *, text: str):
        """Eval some code"""
        await ctx.send(f"```python\n{eval(text)}```")

    @commands.is_owner()
    @commands.command(name='exec', hidden=True)
    async def _exec(self, ctx, *, text: str):
        """Exec some code, used a string instead of a file"""

        old_stdout = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            exec(text)
            buffer.seek(0)
            await ctx.send(f"```python\n{buffer.read()}```")
        except Exception as e:
            await ctx.send(f"```python\n{e}```")
        finally:
            sys.stdout = old_stdout
            del buffer

    @commands.is_owner()
    @commands.command(name='sql', hidden=True)
    async def _sql(self, ctx, *, sql: str):
        """Runs SQL"""
        con = sqlite3.connect("database.db")
        # commit or rollback is automatical, depending of success
        try:
            with con:
                cur = con.cursor()
                results = con.executescript(sql)
                if results:
                    message = f"```python\n{results}```"
                    if len(message) > 2000:
                        await ctx.send("Results too long",
                        file=discord.File(io.BytesIO(fmt.encode('utf-8')),
                        'results.txt'))
                    else:
                        await ctx.send(message)
                else:
                    await ctx.send('\N{SQUARED OK}')
        except Exception as e:
            await ctx.send(e)

    @commands.command( hidden=True)
    async def guildsUpdate(self, ctx):
        """Exec some code, used a string instead of a file"""
        for guild in self.bot.guilds:
            try:
                with self.db_con:
                    self.db_con.execute(f"""INSERT OR IGNORE INTO guilds VALUES
                        ({guild.id}, {guild.name}, 'fr!', '', '')
                    """)
            except sqlite3.IntegrityError:
                print(f"ERROR adding {guild.name} ({guild.id}) to database")

def setup(bot):
    bot.add_cog(Owner(bot))
