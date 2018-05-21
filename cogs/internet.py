import discord
from discord.ext import commands

import stackexchange as se

from config import *

class Internet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['so'])
    async def stackoverflow(self, ctx, *, text: str):
        """Queries StackOverflow and gives you top results"""

        so = se.Site(se.StackOverflow, SE_KEY)
        so.impose_throttling = True
        so.throttle_stop = False

        qs = so.search(intitle=text)[:3]
        if qs:
            emb = discord.Embed(title=text)
            emb.set_thumbnail(url='https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a')
            emb.set_footer(text="Hover for vote stats")

            for q in qs:
                q = so.question(q.id, filter="!b1MME4lS1P-8fK") # Fetch question's data, include vote_counts and answers
                emb.add_field(name=f"`{len(q.answers)} answers` Score : {q.score}",
                value=f'[{q.title}](https://stackoverflow.com/q/{q.id} "{q.up_vote_count}🔺|{q.down_vote_count}🔻")')
            await ctx.send(embed=emb)

        else:
            await ctx.send("No results")

def setup(bot):
    bot.add_cog(Internet(bot))
