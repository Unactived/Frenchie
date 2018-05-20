import discord
from discord.ext import commands

import stackexchange as se

from config.py import *

class Internet:
    def __init__(self, bot):
        self.bot = bot

        so = se.Site(se.StackOverflow, SE_KEY)
        so.impose_throttling = True
        so.throttle_stop = False

    @commands.command(aliases=['so'])
    async def stackoverflow(self, ctx, *, text: str):
        """Querys StackOverflow and gives you top result"""

        qs = so.search(intitle=text)[:3]
        if qs:
            emb = discord.Embed(title=text)
            emb.set_thumbnail(url='https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a')
            emb.set_footer(text="Powered by StackExchange API")

            for q in qs:
                q = so.question(q.id) # Fetch question's data
                emb.add_field(name=f"[{q.title}](https://stackoverflow.com/q/{q.id})", value=f"`{len(q.answers)} answers` Score : {q.score}")

            await ctx.send(embed=emb)

        else:
            await ctx.send("No results")

def setup(bot):
    bot.add_cog(Internet(bot))
