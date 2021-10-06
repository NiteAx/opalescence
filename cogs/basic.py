from discord.ext import commands
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

#Joinrole related
roles=[802170446250115073,802170728538570792,802170902896705536,802171084610076673,802174521993199626,802174717611212870,802174908464496690]
responses=["I just don't know what went wrong! <a:derp:554593471089082378>", "Oops, my bad! <:derpysad:587780328765259776>", "All done! <a:derpysmile:399726352758079498>", "Want a complimentary muffin? <a:derpysmile:399726352758079498>" , "Break time!"]
breaktime=[" <:derpystop:585590699307696159>", " <:derpysleep:588652359450886154>", " <a:derpywave:585560131140452389>"]
repodir = Path('../manechat.github.io')
indexdir = str(repodir / 'invite.txt')
repodir = str(repodir)

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def add(self, ctx, left : int, right : int):
        """Adds two numbers together."""
        await ctx.send("The sum of "+str(left)+" and "+str(right)+" is "+str(left+right)+"!!!!!")

    #bad channel parsing
    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def echo(self, ctx, chanName : str, *, message: str):
        chanName = int(chanName.split("#")[1].split(">")[0])
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

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def remindme(self, ctx, time : int, reminder : str):
        await ctx.send('```Reminder set for '+str(time)+' seconds from now.```')
        await asyncio.sleep(time)
        await ctx.send(reminder)

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
    async def feedback(self, ctx):
        await ctx.author.send("0. At the end of the day, the users are the most important part of our server. Your thoughts and opinions have a lot of weight in our moderation of the server, no matter how small or personal you think the problem is, but most of the time we only get to hear ours. There are several ways you can get in touch and provide feedback and concerns about the server:\na. The Feeling Form (https://forms.gle/9ZQ8veUsJ7JyFr3R8) is private, goes directly to all mods and can be anonymous. But if you sign it, we will always get back to you with a response.\nb. Post in <#819365738543710258>\nc. Direct Message one of the mods\nd. Request Luna's guest to have a real time chat with all the mods at once, alone or accompanied.")

def setup(bot):
    bot.add_cog(Basic(bot))
