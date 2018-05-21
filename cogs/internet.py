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

    @commands.command(usage="<location>,[<country code>]")
    async def weather(self, ctx, location):
        """Gives you current weather stuff on a given city"""
        async with ctx.typing():
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(urllib.parse.quote_plus(weather_url.format(location), safe=';/?:@&=$,><-[]')) as    response:
                    if response.status == 200:
                        data = await response.json()

                        temperature = data['main']['temp']
                        windSpeed = data['wind']['speed']
                        sunrise = str(datetime.utcfromtimestamp(data['sys']['sunrise'])).split(" ")[1]
                        sunset = str(datetime.utcfromtimestamp(data['sys']['sunset'])).split(" ")[1]
                        humidity = data['main']['humidity']
                        pressure = data['main']['pressure']
                        city = data['name'].capitalize()
                        countryFlag = f':flag_{data["sys"]["country"].lower()}:'

                        emb = discord.Embed(title=f"Current weather at {city} {countryFlag} : {data['weather'][0]['description']}", color=BLUE)
                        emb.set_thumbnail(url=earth_url)
                        emb.add_field(name=":thermometer: Temperature",value=f"{temperature} °C")
                        emb.add_field(name=":dash: Wind speed",value=f"{windSpeed} m/s")
                        emb.add_field(name=":sunrise_over_mountains: Sunrise",value=f'{sunrise} (UTC)')
                        emb.add_field(name=":city_sunset: Sunset",value=f'{sunset} (UTC)')
                        emb.add_field(name=":droplet: Humidity",value=f'{humidity} %')
                        emb.add_field(name=":cloud: Pressure",value=f'{pressure} hPa')

                        emb.set_footer(text="powered by openweathermap.org")
                        await ctx.send(embed=emb)
                    else:
                        await ctx.send(f"An error occurred, code : {response.status}. Check your arguments.")

def setup(bot):
    bot.add_cog(Internet(bot))
