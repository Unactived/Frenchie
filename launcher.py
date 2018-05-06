import sys
import logging
import contextlib
import discord
import asyncio

from config import *

from bot import Frenchie, extensions

def run_bot(token):
    loop = asyncio.get_event_loop()
    #log = logging.getLogger()

    # Database setup goes here

    bot = Frenchie()
    bot.run(token)

if __name__ == '__main__':
    run_bot(BOT_TOKEN)
