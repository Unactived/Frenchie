import discord
from discord.ext import commands
import aiohttp, urllib.parse
from datetime import datetime

import stackexchange as se

from config import *

class Internet:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def cpp(self, ctx, *, query: str):
        """Search something on cppreference"""

        url = 'http://en.cppreference.com/w/cpp/index.php'
        params = {
            'title': 'Special:Search',
            'search': query
        }

        async with ctx.session.get(url, params=params) as resp:
            if resp.status != 200:
                return await ctx.send(f'An error occurred (status code: {resp.status}). Retry later.')

            if len(resp.history) > 0:
                return await ctx.send(resp.url)

            e = discord.Embed()
            root = etree.fromstring(await resp.text(), etree.HTMLParser())

            nodes = root.findall(".//div[@class='mw-search-result-heading']/a")

            description = []
            special_pages = []
            for node in nodes:
                href = node.attrib['href']
                if not href.startswith('/w/cpp'):
                    continue

                if href.startswith(('/w/cpp/language', '/w/cpp/concept')):
                    # special page
                    special_pages.append(f'[{node.text}](http://en.cppreference.com{href})')
                else:
                    description.append(f'[`{node.text}`](http://en.cppreference.com{href})')

            if len(special_pages) > 0:
                e.add_field(name='Language Results', value='\n'.join(special_pages), inline=False)
                if len(description):
                    e.add_field(name='Library Results', value='\n'.join(description[:10]), inline=False)
            else:
                if not len(description):
                    return await ctx.send('No results found.')

                e.title = 'Search Results'
                e.description = '\n'.join(description[:15])

            await ctx.send(embed=e)

    @commands.command(aliases=['so'])
    async def stackoverflow(self, ctx, *, text: str):
        """Queries StackOverflow and gives you top results"""

        so = se.Site(se.StackOverflow, SE_KEY)
        so.impose_throttling = True
        so.throttle_stop = False

        async with ctx.typing():
            qs = so.search(intitle=text)[:3]
            if qs:
                emb = discord.Embed(title=text)
                emb.set_thumbnail(url='https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a')
                emb.set_footer(text="Hover for vote stats")

                for q in qs:
                    q = so.question(q.id, filter="!b1MME4lS1P-8fK") # Fetch question's data, include vote_counts and answers
                    emb.add_field(name=f"`{len(q.answers)} answers` Score : {q.score}",
                    value=f'[{q.title}](https://stackoverflow.com/q/{q.id} "{q.up_vote_count}🔺|{q.down_vote_count}🔻")',
                    inline=False)
                await ctx.send(embed=emb)

            else:
                await ctx.send("No results")

    @commands.command(name="run", usage="<language>|[\`\`\`][<language>\n]<code>][\`\`\`]")
    async def run_code(self, ctx, *, text: str):
        """Run code and feedback Output, warnings, errors and performance"""
        arg = text.split('|')
        language = arg[0].capitalize()
        code = arg[1][3:-3]
        #code markdown, C++ and C#/F#
        if code.startswith(arg[0]+'\n'):
            code = code[len(arg[0])+1:]
        elif code.startswith("cpp\n"):
            code = code[4:]
        elif code[1:].startswith('sharp\n'):
            code = code[7:]

        rexUrlRequest = rex_url.format(rexLanguageDict[language], code)
        #TODO: add optional compiler args input # INPUT is useless
        #if len(arg) > 2:
        #    if arg[2].startswith('INPUT='):
        #        rexUrlRequest += '&Input=' + arg[2][6:]
        #    if not arg[-1].startswith('INPUT='):
        #        rexUrlRequest += '&CompilerArgs=' + arg[-1]
        if ('&CompilerArgs' not in rexUrlRequest) and (language in rexCompilerDict):
            rexUrlRequest += '&CompilerArgs=' + rexCompilerDict[language]
        #removing bad URL characters
        rexUrlRequest = urllib.parse.quote_plus(rexUrlRequest, safe=';/?:@&=$,><-[]')
        async with ctx.typing():
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(rexUrlRequest) as response:
                    if response.status == 200:
                        donnees = await response.json()
                        content = ""
                        if donnees['Result']:
                            content += f'```{donnees["Result"]}```'
                        if donnees['Warnings']:
                            content += f'```fix\n{donnees["Warnings"]}```'
                        if donnees['Errors']:
                            # Red markdown
                            listErrors = donnees['Errors'].split('\n')
                            for line in listErrors:
                                listErrors[listErrors.index(line)] = '-' + line
                            if len(listErrors) > 1:
                                donnees['Errors'] = "diff\n" + "\n".join(listErrors)[:-1]
                            else:
                                donnees['Errors'] = "diff\n" + "\n".join(listErrors)

                            content += f'```{donnees["Errors"]}```'
                        if donnees['Stats']:
                            content += f'```{donnees["Stats"]}```'
                        if not content:
                            content = "```No output```"
                        await ctx.send(content)
                    else:
                        await ctx.send(f"An error occurred, code {response.status}\nCommand usage : `.run <language>|```<code>```[|INPUT=<input>][|<compiler args>]`")

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
