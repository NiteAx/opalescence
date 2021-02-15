from discord.ext import commands, tasks
import discord
from discord.utils import get
import sys
sys.path.append('..')
from config import *
import asyncio
import random
from datetime import datetime
import re
import subprocess
from pathlib import Path
import io
import aiohttp
from itertools import cycle

#Joinrole related
roles=[802170446250115073,802170728538570792,802170902896705536,802171084610076673,802174521993199626,802174717611212870,802174908464496690]
responses=["I just don't know what went wrong! <a:derp:554593471089082378>", "Oops, my bad! <:derpysad:587780328765259776>", "All done! <a:derpysmile:399726352758079498>", "Want a complimentary muffin? <a:derpysmile:399726352758079498>" , "Break time!"]
breaktime=[" <:derpystop:585590699307696159>", " <:derpysleep:588652359450886154>", " <a:derpywave:585560131140452389>"]
bannerbucket = []
guild_id = 98609319519453184
repodir = Path('../manechat.github.io')
indexdir = str(repodir / 'invite.txt')
repodir = str(repodir)
pingtime = 60

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.set_random_banner.start()

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def add(self, ctx, left : int, right : int):
        """Adds two numbers together."""
        await ctx.send(left + right)
    
    #bad channel parsing
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def echo(self, ctx, chanName : str, *, message: str):
        chanName = chanName.split('#').pop()
        if chanName.endswith('>'):
            chanName = chanName.split('>')[0]
        await self.bot.get_channel(chanName).send(message)
    
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def echomc(self, ctx, *, message: str):
        await self.bot.get_channel(98609319519453184).send(message)
    
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def repeat(self, ctx, times : int, content : str):
        """Repeats a message multiple times."""
        if times < 6:
            for i in range(times):
                await ctx.send(content)
        else:
            await ctx.send("Please don't get me banned by Discord! (Max 5)")
    
    @commands.command(pass_context=True)
    @commands.has_any_role(*Whitelist)
    async def roleid(self, ctx, *, rolename : str):
        roles = ctx.message.guild.roles
        for role in (y for y in roles if y.name.lower() == rolename.lower()):
            print(role.name+': '+str(role.id)) 
            await ctx.send('```'+role.name+': '+str(role.id)+'```')

    @commands.command(pass_context=True)
    @commands.has_any_role(*Whitelist)
    async def listroles(self, ctx):
        roles = ctx.message.guild.roles
        for role in (y for y in roles if y.name != '@everyone'):
            print(role.name +' '+ str(role.id))
    
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def remindme(self, ctx, time : int, reminder : str):
        await ctx.send('```Reminder set for '+str(time)+' seconds from now.```')
        await asyncio.sleep(time)
        await ctx.send(reminder)
    
    @commands.command(pass_context=True)
    async def joinrole(self, ctx):
        chosenrole = ctx.message.guild.get_role(random.choice(roles))
        print('Random Role: '+chosenrole.name+' '+str(chosenrole.id))
        user = ctx.message.author
        memberoles = []
        for role in user.roles:
            memberoles.append(role.id)
        #print("Member Role ID's:")
        #print(memberoles)
        if set(roles).isdisjoint(set(memberoles)):
            await user.add_roles(chosenrole)
    
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def stowaways(self, ctx):
        stowaways = "Stowaways:\n"
        for member in self.bot.get_guild(98609319519453184).members:
            roles = []
            for role in member.roles:
                roles.append(role.name)
            if discord.utils.get(self.bot.get_guild(98609319519453184).roles, id=552450130633031700).name not in roles:
                stowaways += member.mention+'\n'
        print(stowaways)
        if stowaways == "Stowaways:\n":
            await ctx.send("Hull's clear, cap'n.")
        else:
            await ctx.send(stowaways)
    
    @commands.command(pass_context=True)
    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)
    async def ping(self, ctx, *, role : str):
        if ctx.message.author.top_role.name == 'Mods':
                    ctx.command.reset_cooldown(ctx)
        if ctx.message.author.top_role.id != newprole: #ignore newp
            if any(pingrole.lower() == role.lower() for pingrole in pingwhitelist):
                print('['+(str(datetime.now())).split('.')[0]+' UTC] '+ctx.message.author.name+' used ?ping '+role)
                roles = ctx.message.guild.roles
                roles = [r.name for r in roles]
                for r in (y for y in roles if y.lower() == role.lower()):
                    pingrole = r
                r = pingrole
                pingrole = discord.utils.get(ctx.message.guild.roles, name=r)
                await pingrole.edit(mentionable=True)
                nowpingable = await ctx.send('```'+r+' is now pingable for '+str(pingtime)+' seconds.```')
                await asyncio.sleep(pingtime)
                await pingrole.edit(mentionable=False)
                await ctx.message.delete()
                await nowpingable.delete()
            else:
                print(ctx.message.author.name+' failed to use ?ping '+role+' at '+str(datetime.datetime.now()))
                notwhitelisted = await ctx.send('```'+role+' is not whitelisted.```')
                ctx.command.reset_cooldown(ctx)
                await asyncio.sleep(5)
                await ctx.message.delete()
                await notwhitelisted.delete()
                
    @commands.command(pass_context=True)
    @commands.has_any_role(*Whitelist)
    async def rotate(self, ctx):
        print(ctx.message.author.name+' used ?rotate at '+str(datetime.datetime.now()))
        print('----Pulling repo')
        subprocess.call(["git", "-C", repodir, "pull"]) #git pull repo
        with open(indexdir, 'r') as f: #find homepage invite from index.html
            invitetxt = f.read()
            print('invitetxt = '+invitetxt)
        discord_inviteURL = invitetxt
        discord_invitecode = discord_inviteURL.split('discord.gg/')[1]
        print('discord_invitecode = '+discord_invitecode)
        try:
            invite = await self.bot.fetch_invite(discord_inviteURL)
            await invite.delete() #await delete invite 
            message = await ctx.send('```Rotating invite...```')
            invite = await self.bot.get_channel(648943910013501448).create_invite(max_age=0, unique=True) #create new invite
            new_invitetxt = invitetxt.replace(discord_invitecode, invite.code)
            with open(indexdir, 'w') as file: #replace invite index.html
                file.write(new_invitetxt)   
            #git push to remote
            print('----Adding changes')
            subprocess.call(["git", "-C", repodir, "add", "-u",])
            print('----Comitting')
            subprocess.call(["git", "-C", repodir, "commit", "-m", "Rotate the invite link"])
            print('----Pushing to remote')
            subprocess.call(["git", "-C", repodir, "push"])
            await message.edit(content='```Rotated invite.```')
        except:
            print('Mistmatch between repo and current server invite.')
            await ctx.send('```Mistmatch between repo and current server invite.```')
        
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def setbanner(self, ctx, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("```Problem downloading file.```")
                data = io.BytesIO(await resp.read())
                await ctx.message.guild.edit(banner=data.read())
                await ctx.send("```Banner set.```")
                
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def addbanner(self, ctx, url:str):
        bannerbucket.append(url)
        bannerlist = "```Banner URLs:\n"
        for x in bannerbucket:
            bannerlist += x+'\n'
        bannerlist += "```"
        #print(bannerlist)
        await ctx.send(bannerlist)
        
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def listbanner(self, ctx):
        bannerlist = "```Banner URLs:\n"
        for x in bannerbucket:
            bannerlist += x+'\n'
        bannerlist += "```"
        #print(bannerlist)
        await ctx.send(bannerlist)
        
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def clearbanner(self, ctx):
        bannerbucket.clear()
        await ctx.send("```Banners cleared.```")
        
    @tasks.loop(hours=1.0)
    async def set_random_banner(self):
        guild = self.bot.get_guild(guild_id)
        if len(bannerbucket) > 0:
            url = random.choice(bannerbucket)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        print("Problem downloading file.")
                    data = io.BytesIO(await resp.read())
                    await guild.edit(banner=data.read())
                    print("Banner set to "+url)
    
def setup(bot):
    bot.add_cog(Basic(bot))