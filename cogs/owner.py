import discord
from discord.ext import commands
import traceback
from contextlib import redirect_stdout
import textwrap
import os
import io
import sqlite3

# from checks import *


class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.db_con = sqlite3.connect('database.db')
        self._last_eval_result = None

    # Owner check
    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(aliases=['streaming', 'listening', 'watching'], hidden=True)
    async def playing(self, ctx, media=f'fr!info | fr!help'):
        """Update bot presence accordingly to invoke command"""
        # Need URL for streaming
        p_types = {'playing': 0, 'streaming': 1, 'listening': 2, 'watching': 3}
        activity = discord.Activity(name=media, type=p_types[ctx.invoked_with])

        await self.bot.change_presence(activity=activity)

    @commands.command(hidden=True)
    async def guildlist(self, ctx):
        """Displays all guilds the bot is on and their members amount"""
        text = "**Frenchie's server list** :\n"
        for guild in self.bot.guilds[:50]:
            text += f'**{guild.name}**, {guild.member_count} members\n'
        await ctx.send(text)

    @commands.command(hidden=True)
    async def guildinfo(self, ctx, guild: str):
        """Displays stuff on a given guild, and an invite if possible"""
        guild = discord.utils.get(self.bot.guilds, name=guild)
        emb = discord.Embed(title=f"{guild.name}", color=BLUE)
        emb.set_thumbnail(url=guild.icon_url)
        emb.add_field(name="Region", value=f'{guild.region}')
        emb.add_field(name="Members", value=guild.member_count)
        try:
            invite = await guild.text_channels[0].create_invite(unique=False)
            invite_link = f"[invite](https://discord.gg/{invite.code})"
        except Exception as e:
            invite_link = e
        emb.add_field(name="Invite", value=invite_link)

        await ctx.send(embed=emb)

    @commands.command(hidden=True)
    async def load(self, ctx, *, extension):
        """Loads a cog"""
        try:
            self.bot.load_extension(extension)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{SQUARED OK}')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, extension):
        """Unloads a cog"""
        try:
            self.bot.unload_extension(extension)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send('\N{SQUARED OK}')

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, extension):
        """Reloads a module."""
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        except Exception:
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
        os.system(f'./redeploy.sh {branch}')  # Reload Github and bot

    @commands.guild_only()
    @commands.command(hidden=True)
    async def say(self, ctx, channel: discord.TextChannel, *, text: str):
        """Makes the bot say something in a given current guild's channel"""
        await channel.send(text)

    def _clean_code(self, code):
        # Markdown py ; not python
        if code.startswith('```') and code.endswith('```'):
            return '\n'.join(code.split('\n')[1:-1])
        return code.strip('`\n')

    @commands.is_owner()
    @commands.command(name='eval', hidden=True)
    async def _eval(self, ctx, *, code: str):
        """Eval some code"""

        env = {
            'db_con': self.db_con,
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'message': ctx.message,
            '_': self._last_eval_result
        }
        env.update(globals())

        code = self._clean_code(code)
        buffer = io.StringIO()

        # function placeholder
        to_compile = f'async def foo():\n{textwrap.indent(code, " ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n``')

        foo = env['foo']
        try:
            with redirect_stdout(buffer):
                ret = await foo()
        except Exception:
            value = buffer.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = buffer.getvalue()
            try:
                await ctx.message.add_reaction('\N{INCOMING ENVELOPE}')
            except Exception:
                # well...
                pass

            if ret is None:
                if value is not None:
                    await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Owner(bot))
