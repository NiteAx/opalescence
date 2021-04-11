import discord
from discord.utils import get
from discord.ext import commands, tasks
import random
import io
import aiohttp
import sys
sys.path.append('..')
from config import *

current_banner = ""

class Banner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.set_random_banner.start()

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def addbanner(self, ctx, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(str(resp.status))
        if resp.status != 200:
            print("Problem getting file."")
            await ctx.send("```Problem getting file.```")
        else:
            data = io.BytesIO(await resp.read())
            await guild.edit(banner=data.read())
            print("Banner set to "+current_banner)

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def addbanner(self, ctx, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                print(str(resp.status))
        if resp.status != 200:
            print("Problem getting file."")
            await ctx.send("```Problem getting file.```")
        else:
            with open('bannerlist.txt', 'a+') as f:
                f.write(url+"\n")
                f.close
            f = open ('bannerlist.txt', 'r')
            contents = f.read()
            print(contents)
            await ctx.send("```Banner list:\n"+contents+"```")

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def listbanner(self, ctx):
        f = open ('bannerlist.txt', 'r')
        contents = f.read()
        print(contents)
        await ctx.send("```Banner list:\n"+contents+"```")

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def clearbanner(self, ctx):
        with open('bannerlist.txt', 'w') as f:
            print("Cleared bannerlist.txt")
            f.close

    @commands.command()
    async def banner(self, ctx):
        global current_banner
        #print(current_banner)
        if len(current_banner) > 0:
            await ctx.send(str(current_banner))
        else:
            await ctx.send(str("```Banner not currently set.```"))

    @tasks.loop(seconds=5)
    async def set_random_banner(self):
        global current_banner
        guild = self.bot.get_guild(guild_id)
        f = open ('bannerlist.txt', 'r')
        contents = f.read()
        bannerlist = contents.splitlines(True)
        if len(contents) > 0:
            #print(bannerlist)
            current_banner = random.choice([i for i in bannerlist if i != current_banner])
            current_banner = current_banner.split('\n')[0]
            print(current_banner)
            async with aiohttp.ClientSession() as session:
                async with session.get(current_banner) as resp:
                    if resp.status != 200:
                        print("Problem downloading file: "+str(resp.status))
                    else:
                        try:
                            data = io.BytesIO(await resp.read())
                            await guild.edit(banner=data.read())
                            print("Banner set to "+current_banner)
                        except:
                            print("Problem setting banner.")

    @set_random_banner.before_loop
    async def before_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Banner(bot))
