#import asyncio
import discord
from discord.ext import commands
import urllib.parse

from config import *
from checks import *

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Some info about the bot, including an invite link"""

        description = """FrenchMasterSword's bot, provides some cool utilities (just to be sure,\
it's French, and still in development)"""

        embed = discord.Embed(title="Frenchie", description=description, color=BLUE)

        embed.add_field(name="Author", value="FrenchMasterSword#9035")
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Invite", value=f'[Invite me to your server !]({invite_url} "What are you waiting for ?")')
        embed.add_field(name="Bug report", value=f"[Please open an issue]({invite_url}/issues)")
        embed.set_footer(text="Coded with ❤ and Python 3")

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Gives you the bot's latency"""
        latency = round(self.bot.latency * 1000, 2)

        await ctx.send(f':ping_pong: **Pong !** Latency : `{latency} ms`')

    @commands.command(aliases=['source'])
    async def sourcecode(self, ctx):
        """Grants you access to a horrible code which strikes you blind"""
        emb = discord.Embed(title="Frenchie", description="Legend tells that if you\
 do not star this repository, you finish eaten by a baguette", color=BLUE)
        emb.add_field(name="Beware", value=f'[Source code (Github)]({source_url} "⭐?")')
        emb.set_footer(text="If you find this bot useful, don't forget the ⭐ ^^")

        await ctx.send(embed=emb)

    @commands.command()
    async def runlist(self, ctx):
        """Supported languages by the run command"""
        emb = discord.Embed(title="List of supported languages by run command",\
        description="An exhaustive list is available [here](https://hastebin.com/pojukacafa.vbs)", color=BLUE)

        await ctx.send(embed=emb)

    @commands.group(hidden=True)
    async def ask(self, ctx):
        """Searches on the given website"""
        if ctx.invoked_subcommand is None:

            await ctx.send(f'Usage : `{prefix}ask <site> "Arguments"`')

    @commands.command()
    async def lmgtfy(self, ctx, *, text: str):
        """Teaches you Internet"""

        url = f"http://lmgtfy.com/?q={text}"
        url = urllib.parse.quote_plus(url, safe=';/?:@&=$,><-[]')
        emb = discord.Embed(title="How it works", description=f"[{text}]({url})", color=BLUE)

        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(General(bot))
