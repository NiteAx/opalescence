from discord.ext import commands
import discord
from discord.utils import get
import sys
sys.path.append('..')
from config import *
import asyncio
import random
import datetime
import re
import subprocess
from pathlib import Path

roles=['672990112774094898','672990213986844712','672990221855490058','672990225047486464','672990228901789716','672990232488181810','672990235558412291']
repodir = Path('../manechat.github.io')
indexdir = str(repodir / 'invite.txt')
repodir = str(repodir)
pingtime = 60

class Basic():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def echo(self, ctx, chanName : str, *, message: str):
        chanName = chanName.split('#').pop()
        if chanName.endswith('>'):
            chanName = chanName.split('>')[0]
            chan = discord.utils.get(ctx.message.server.channels, id=chanName)
        else:
            chan = discord.utils.get(ctx.message.server.channels, name=chanName)
        await self.bot.send_message(chan, message)
    
    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def echomc(self, *, message: str):
        await self.bot.send_message(self.bot.get_channel('98609319519453184'), message)
    
    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def add(self, left : int, right : int):
        """Adds two numbers together."""
        await self.bot.say(left + right)

    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def repeat(self,  times : int, content : str):
        """Repeats a message multiple times."""
        if times < 6:
            for i in range(times):
                await self.bot.say(content)
        else:
            await self.bot.say("Please don't get me banned by Discord!")
    
    @commands.command(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie') 
    async def listrole(self, ctx, *, rolename : str):
        roles = ctx.message.server.roles
        for role in (y for y in roles if y.name.lower() == rolename.lower()):
            print(role.name+': '+role.id) 
            await self.bot.say('```'+role.name+': '+role.id+'```')

    @commands.command(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie') 
    async def listroles(self, ctx):
        roles = ctx.message.server.roles
        for role in (y for y in roles if y.name != '@everyone'):
            print(role.name +' '+ role.id)
    
    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def remindme(self, time : int, reminder : str):
        await self.bot.say('```Reminder set for '+str(time)+' seconds from now.```')
        await asyncio.sleep(time)
        await self.bot.say(reminder)
    
    @commands.command(pass_context=True, aliases=['dashmyrainbow','20%cooler','awwyeah','rainbowdash','rdwut','ceruleanblue',"I'mshaking"])
    async def joinrole(self, ctx):
        chosenrole = discord.utils.get(ctx.message.server.roles, id=random.choice(roles))
        #print('Random Role: '+chosenrole.name+' '+chosenrole.id)
        user = ctx.message.author
        memberoles = []
        for role in user.roles:
            memberoles.append(role.id)
        #print("Member Role ID's:")
        #print(memberoles)
        if set(roles).isdisjoint(set(memberoles)):
            await self.bot.add_roles(user, chosenrole)
            #print('Assigning role....')
        #else:
            #print('User already has role from list.')
    
    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def stowaways(self):
        stowaways = "Stowaways:\n"
        for member in self.bot.get_server('98609319519453184').members:
            roles = []
            for role in member.roles:
                roles.append(role.name)
            if discord.utils.get(self.bot.get_server('98609319519453184').roles, id='552450130633031700').name not in roles:
                stowaways += member.mention+'\n'
        print(stowaways)
        if stowaways == "Stowaways:\n":
            await self.bot.say("Hull's clear, cap'n.")
        else:
            await self.bot.say(stowaways)
    
    @commands.command(pass_context=True)
    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)
    async def ping(self, ctx, *, role : str):
        if ctx.message.author.top_role.name == 'Mods':
                    ctx.command.reset_cooldown(ctx)
        if ctx.message.author.top_role.id != newprole: #ignore newp
            if any(pingrole.lower() == role.lower() for pingrole in pingwhitelist):
                print(ctx.message.author.name+' used ?ping'+role+' at '+str(datetime.datetime.now()))
                roles = ctx.message.server.roles
                roles = [r.name for r in roles]
                for r in (y for y in roles if y.lower() == role.lower()):
                    pingrole = r
                r = pingrole
                pingrole = discord.utils.get(ctx.message.server.roles, name=r)
                await self.bot.edit_role(ctx.message.server, pingrole, mentionable=True)
                nowpingable = await self.bot.say('```'+r+' is now pingable for '+str(pingtime)+' seconds.```')
                await asyncio.sleep(pingtime)
                await self.bot.edit_role(ctx.message.server, pingrole, mentionable=False)
                await self.bot.delete_message(ctx.message)
                await self.bot.delete_message(nowpingable)
            else:
                print(ctx.message.author.name+' failed to use ?ping '+role+' at '+str(datetime.datetime.now()))
                notwhitelisted = await self.bot.say('```'+role+' is not whitelisted.```')
                ctx.command.reset_cooldown(ctx)
                await asyncio.sleep(5)
                await self.bot.delete_message(ctx.message)
                await self.bot.delete_message(notwhitelisted)
                
    @commands.command(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
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
            invite = await self.bot.get_invite(discord_inviteURL)
            await self.bot.delete_invite(invite) #await delete invite 
            message = await self.bot.send_message(ctx.message.channel, '```Rotating invite...```')
            invite = await self.bot.create_invite(self.bot.get_channel('648943910013501448'), max_age=0, unqiue=True) #create new invite
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
            await self.bot.edit_message(message, '```Rotated invite.```')
        except:
            print('Mistmatch between repo and current server invite.')
            await self.bot.send_message(ctx.message.channel, '```Mistmatch between repo and current server invite.```')
        
def setup(bot):
    bot.add_cog(Basic(bot))