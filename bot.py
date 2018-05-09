import sys

#import asyncio
import discord
from discord.ext import commands

from config import *

description = """
FrenchMasterSword's bot, provides some cool utilities (just to be sure,\
 it's French, and still in development)
"""

extensions = (
    'cogs.admin',
    'cogs.general',
    'cogs.music',
    'cogs.owner',
)

class Frenchie(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(prefix),
        description=description, pm_help=None)

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                #print in error stream
                print(f"Couldn't load the following extension : {extension} ; :{e}", file=sys.stderr)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} ; ID : {self.user.id}')
        print('-----------------------------------------------\n')
        await self.change_presence(status=3,
        activity=discord.Game(name=f'{prefix}info | {prefix}help'))

    async def on_resumed(self):
        print(f'\n[*] {self.user} resumed...')

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self, token):
        super().run(token, reconnect=True)
