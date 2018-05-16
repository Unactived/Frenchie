import sys
import logging
import contextlib
import discord
import asyncio
import sqlite3

from config import *

from bot import Frenchie, extensions

def run_bot(token):
    loop = asyncio.get_event_loop()
    #log = logging.getLogger()

    db_con = sqlite3.connect('database.db')
    try:
        with db_con:
            db_con.execute(f"""CREATE TABLE IF NOT EXISTS guilds
                (id integer UNIQUE, name text, prefix text, msg_join text,
                msg_leave text, creation text, lang text)
            """)
    except sqlite3.IntegrityError:
        print(f"ERROR creating guilds table in database")

    bot = Frenchie()
    bot.run(token)

if __name__ == '__main__':
    run_bot(BOT_TOKEN)
