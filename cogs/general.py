#import asyncio
import discord
from discord.ext import commands
import aiohttp, urllib.parse
from datetime import datetime
import os
import stackexchange

from config import *
from checks import *

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Some info about the bot, including an invite link"""

        description = """FrenchMasterSword's bot, provides some cool utilities (just to be sure,\
it's French, and still in development)"""

        embed = discord.Embed(title="Frenchie", description=description, color=BLUE)

        embed.add_field(name="Author", value="FrenchMasterSword#9035")
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Invite", value=f"[Invite me to your server !]({invite_url})")
        embed.add_field(name="Bug report", value=f"[Please open an issue]({invite_url}/issues)")
        embed.set_footer(text="Coded with ❤ and Python 3")

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Gives you the bot's latency"""
        latency = round(self.bot.latency * 1000, 2)

        await ctx.send(f':ping_pong: **Pong !** Latency : `{latency} ms`')

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

    @commands.command(aliases=['source'])
    async def sourcecode(self, ctx):
        """Grants you access to a horrible code which strikes you blind"""
        emb = discord.Embed(title="Frenchie", description="Legend tells that if you\
 do not star this repository, you finish eaten by a baguette", color=BLUE)
        emb.add_field(name="Beware", value=f"[Source code (Github)]({source_url})")
        emb.set_footer(text="If you find this bot useful, don't forget the ⭐ ^^")

        await ctx.send(embed=emb)

    @commands.command()
    async def runlist(self, ctx):
        """Supported languages by the run command"""
        emb = discord.Embed(title="List of supported languages by run command",\
        description="An exhaustive list is available [here](https://hastebin.com/pojukacafa.vbs)", color=BLUE)

        await ctx.send(embed=emb)

    @commands.group(hidden=True)
    async def ask(self, ctx):
        """Searches on the given website"""
        if ctx.invoked_subcommand is None:

            await ctx.send(f'Usage : `{prefix}ask <site> "Arguments"`')

    @ask.command()
    async def StackOverflow(self, ctx, arg):
        """Subcommand of group ask ; searches on StackOverflow"""

        site = stackexchange.Site(eval(f"stackexchange.{ctx.invoked_with}"),
        app_key=SE_KEY, impose_throttling=True)

        qs = so.search(intitle=arg)

def setup(bot):
    bot.add_cog(General(bot))
