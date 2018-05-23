# import asyncio
import json
# import os
from bot import Frenchie

# Keys and token
with open('private.json') as file:
    configDict = json.load(file)


def run_bot(token):
    # loop = asyncio.get_event_loop()
    # log = logging.getLogger()

    bot = Frenchie()
    bot.run(token)


if __name__ == '__main__':
    BOT_TOKEN = configDict['BOT_TOKEN']
    run_bot(BOT_TOKEN)
