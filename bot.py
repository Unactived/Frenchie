import sys
import sqlite3

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

        self.db_con = sqlite3.connect("database.db")

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

    async def on_guild_join(self, guild):
        try:
            with self.db_con:
                self.db_con.execute(f"""INSERT OR IGNORE INTO guilds VALUES
                    ({guild.id}, {guild.name}, 'fr!', '', '', {guild.created_at}, 'EN')
                """)
        except sqlite3.IntegrityError:
            print(f"ERROR adding {guild.name} ({guild.id}) to database")

    async def on_guild_update(self, before, after):
        try:
            with self.db_con:
                # We assume guild ID won't change
                self.db_con.execute(f"""UPDATE guilds
                    SET name = {after.name} WHERE id = {guild.id}
                """)
                # Add relevant guild updates here
        except sqlite3.IntegrityError:
            print(f"ERROR updating {guild.name} ({guild.id}) in database")

    async def on_guild_remove(self, guild):
        try:
            with self.db_con:
                self.db_con.execute(f"""DELETE FROM guilds
                    WHERE id = {guild.id}
                """)
        except sqlite3.IntegrityError:
            print(f"ERROR removing {guild.name} ({guild.id}) from database")

    async def close(self):
        await super().close()

    def run(self, token):
        super().run(token, reconnect=True)
