import discord
from discord.ext import commands
import sqlite3

def get_guild_attr(guild, attr):
    attrList = ['id', 'name', 'prefix', 'msg_join', 'msg_leave', 'creation', 'lang']
    try:
        with sqlite3.connect('database.db'):
            result = db_con.execute("SELECT * FROM guilds WHERE id=?", [(ctx.guild.id)]).fetchone()
        return result[attrList.index(attr)]

    except Exception as e:
        print(e)
