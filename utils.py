# import discord
# from discord.ext import commands
import sqlite3


def get_guild_attr(guild, attr):
    attrList = ['id', 'name', 'prefix', 'msg_join', 'msg_leave', 'creation', 'lang']
    try:
        with sqlite3.connect('database.db') as db_con:
            result = db_con.execute("SELECT * FROM guilds WHERE id=?", [(guild.id)]).fetchone()
        return result[attrList.index(attr)]

    except Exception as e:
        print(e)
