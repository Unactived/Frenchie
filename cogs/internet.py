import discord
from discord.ext import commands
import aiohttp
import urllib.parse
import json
from datetime import datetime
import random

import stackexchange as se


class Internet:
    def __init__(self, bot):
        # Keys and token
        with open('private.json') as file:
            configDict = json.load(file)

        self.bot = bot
        self.WEATHER_KEY = configDict['WEATHER_KEY']
        self.SE_KEY = configDict['SE_KEY']

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
                return await ctx.send('An error occurred (status code: {resp.status}). Retry later.')

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

        so = se.Site(se.StackOverflow, self.SE_KEY)
        so.impose_throttling = True
        so.throttle_stop = False

        async with ctx.typing():
            qs = so.search(intitle=text)[:3]
            if qs:
                emb = discord.Embed(title=text)
                emb.set_thumbnail(url='https://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a')
                emb.set_footer(text="Hover for vote stats")

                for q in qs:
                    # Fetch question's data, include vote_counts and answers
                    q = so.question(q.id, filter="!b1MME4lS1P-8fK")
                    emb.add_field(name=f"`{len(q.answers)} answers` Score : {q.score}",
                                  value=f'[{q.title}](https://stackoverflow.com/q/{q.id}'
                                        f' "{q.up_vote_count}🔺|{q.down_vote_count}🔻")',
                                  inline=False)

                await ctx.send(embed=emb)
            else:
                await ctx.send("No results")

    @commands.command(name="run", usage=r"<language>|[\`\`\`][<language>\n]<code>][\`\`\`]")
    async def run_code(self, ctx, *, text: str):
        """Run code and feedback Output, warnings, errors and performance"""

        rex_url = 'http://rextester.com/rundotnet/api?LanguageChoice={}&Program={}'
        rexLanguageDict = {'C#': 1, 'Vb.net': 2, 'F#': 3, 'Java': 4, 'Python2': 5,
                           'C': 6, 'C++': 7, 'Php': 8, 'Pascal': 9,
                           'Objective-c': 10, 'Haskell': 11, 'Ruby': 12,
                           'Perl': 13, 'Lua': 14, 'Nasm': 15, 'Sql server': 16,
                           'Javascript': 17, 'Lisp': 18, 'Prolog': 19, 'Go': 20,
                           'Scala': 21, 'Scheme': 22, 'Node.js': 23, 'Python': 24,
                           'Octave': 25, 'C clang': 26, 'C++ clang': 27,
                           'Visual c++': 28, 'Visual c': 29, 'D': 30, 'R': 31,
                           'Tcl': 32, 'Mysql': 33, 'Postgresql': 34, 'Oracle': 35,
                           'Swift': 37, 'Bash': 38, 'Ada': 39, 'Erlang': 40,
                           'Elixir': 41, 'Ocaml': 42, 'Kotlin': 43, 'Brainfuck': 44,
                           'Bf': 44, 'Fortran': 45}

        rexCompilerDict = {'C++': '-Wall -std=c++17 -O2 -o a.out source_file.cpp',
                           'C++ clang': '-Wall -std=c++17 -stdlib=libc++ -O2 -o a.out source_file.cpp',
                           'Visual c++': 'source_file.cpp -o a.exe /EHsc /MD /I C:\boost_1_60_0 /link /LIBPATH:C:\boost_1_60_0\\stage\\lib',
                           'C': '-Wall -std=gnu99 -O2 -o a.out source_file.c',
                           'C clang': '-Wall -std=gnu99 -O2 -o a.out source_file.c',
                           'Visual c': 'source_file.c -o a.exe',
                           'D': 'source_file.d -ofa.out',
                           'Go': '-o a.out source_file.go',
                           'Haskell': '-o a.out source_file.hs',
                           'Objective-c': '-MMD -MP -DGNUSTEP -DGNUSTEP_BASE_LIBRARY=1 -DGNU_GUI_LIBRARY=1 -DGNU_RUNTIME=1 -DGNUSTEP_BASE_LIBRARY=1 -fno-strict-aliasing -fexceptions -fobjc-exceptions -D_NATIVE_OBJC_EXCEPTIONS -pthread -fPIC -Wall -DGSWARN -DGSDIAGNOSE -Wno-import -g -O2 -fgnu-runtime -fconstant-string-class=NSConstantString -I. -I /usr/include/GNUstep -I/usr/include/GNUstep -o a.out source_file.m -lobjc -lgnustep-base'
                           }

        arg = text.split('|')
        language = arg[0].capitalize()
        code = arg[1][3:-3]
        # code markdown, C++ and C#/F#
        if code.startswith(arg[0]+'\n'):
            code = code[len(arg[0])+1:]
        elif code.startswith("cpp\n"):
            code = code[4:]
        elif code[1:].startswith('sharp\n'):
            code = code[7:]

        rexUrlRequest = rex_url.format(rexLanguageDict[language], code)
        # TODO: add optional compiler args input # INPUT is useless
        # if len(arg) > 2:
        #    if arg[2].startswith('INPUT='):
        #        rexUrlRequest += '&Input=' + arg[2][6:]
        #    if not arg[-1].startswith('INPUT='):
        #        rexUrlRequest += '&CompilerArgs=' + arg[-1]
        if ('&CompilerArgs' not in rexUrlRequest) and (language in rexCompilerDict):
            rexUrlRequest += '&CompilerArgs=' + rexCompilerDict[language]
        # removing bad URL characters
        rexUrlRequest = urllib.parse.quote_plus(rexUrlRequest, safe=';/?:@&=$,><-[]')
        async with ctx.typing():
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(rexUrlRequest) as response:
                    if response.status == 200:
                        donnees = await response.json()
                        content = ""
                        if donnees['Result']:
                            content += f'```placeholder\n{donnees["Result"]}```'
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

        weather_url = ('http://api.openweathermap.org/data/2.5/weather?q={}'
                       + f'&appid={self.WEATHER_KEY}&units=metric')

        earth_url = "https://emojipedia-us.s3.amazonaws.com/thumbs/320/twitter"
        "/134/earth-globe-europe-africa_1f30d.png"

        async with ctx.typing():
            async with aiohttp.ClientSession() as client_session:
                url = urllib.parse.quote_plus(weather_url.format(location), safe=';/?:@&=$,><-[]')
                async with client_session.get(url) as response:
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

                        emb = discord.Embed(title=f"Current weather at {city} {countryFlag} "
                                            f": {data['weather'][0]['description']}", color=BLUE)
                        emb.set_thumbnail(url=earth_url)
                        emb.add_field(name=":thermometer: Temperature", value=f"{temperature} °C")
                        emb.add_field(name=":dash: Wind speed", value=f"{windSpeed} m/s")
                        emb.add_field(name=":sunrise_over_mountains: Sunrise", value=f'{sunrise} (UTC)')
                        emb.add_field(name=":city_sunset: Sunset", value=f'{sunset} (UTC)')
                        emb.add_field(name=":droplet: Humidity", value=f'{humidity} %')
                        emb.add_field(name=":cloud: Pressure", value=f'{pressure} hPa')

                        emb.set_footer(text="powered by openweathermap.org")
                        await ctx.send(embed=emb)
                    else:
                        await ctx.send(f"An error occurred, code : {response.status}. Check your arguments.")

    @commands.command()
    async def xkcd(self, ctx, number=None):
        """Sends a given or random xkcd comics"""
        if number is None:
            number = random.randint(0, 1996)
        await ctx.send(f"https://xkcd.com/{number}")


def setup(bot):
    bot.add_cog(Internet(bot))
