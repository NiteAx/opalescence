from discord.ext import commands
import discord
from discord.utils import get

import asyncio
import random
import datetime
import re
import subprocess
from pathlib import Path

# Config is private
import sys
sys.path.append(abspath('..'))  # common.py
sys.path.append(abspath('../..'))  # config.py
from config import *
from common import *

roles = ['540526908794732545',
         '540526928445177858',
         '540526948493819933',
         '540526971222753291',
         '540526982170017802',
         '540526992752246786',
         '540527002483163157']

repodir = Path('../manechat.github.io')
indexdir = str(repodir / 'index.html')
repodir = str(repodir)
pingtime = 60

class Basic():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*admin_roles)
    async def echo(self, chanID : str, message: str):
        await self.bot.send_message(self.bot.get_channel(chanID), message)

    @commands.command()
    @commands.has_any_role(*admin_roles)
    async def add(self, left : int, right : int):
        """Adds two numbers together."""
        await self.bot.say(left + right)

    @commands.command()
    @commands.has_any_role(*admin_roles)
    async def repeat(self,  times : int, content : str):
        """Repeats a message multiple times."""
        if times < 6:
            for i in range(times):
                await self.bot.say(content)
        else:
            await self.bot.say("Please don't get me banned by Discord!")

    @commands.command(pass_context=True)
    @commands.has_any_role(*admin_roles) 
    async def listrole(self, ctx, *, rolename : str):
        roles = ctx.message.server.roles
        for role in (y for y in roles if y.name.lower() == rolename.lower()):
            print(role.name+': '+role.id) 
            await self.bot.say('```'+role.name+': '+role.id+'```')

    @commands.command(pass_context=True)
    @commands.has_any_role(*admin_roles) 
    async def listroles(self, ctx):
        roles = ctx.message.server.roles
        for role in (y for y in roles if y.name != '@everyone'):
            print(role.name +' '+ role.id)

    @commands.command()
    @commands.has_any_role(*admin_roles)
    async def remindme(self, time : int, reminder : str):
        await self.bot.say('```Reminder set for %s seconds from now.```' % time)
        await asyncio.sleep(time)
        await self.bot.say(reminder)

""" DISABLED
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
"""

    @commands.command(pass_context=True)
    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)
    async def ping(self, ctx, *, role : str):
        if ctx.message.author.top_role.name == 'Mods':
            ctx.command.reset_cooldown(ctx)

        if ctx.message.author.top_role.id != newprole: #ignore newp
            if any(pingrole.lower() == role.lower() for pingrole in pingwhitelist):
                print('%s used ?ping %s at %s' % (ctx.message.author.name, role, datetime.datetime.now()))
                roles = ctx.message.server.roles
                for r in (y.name for y in roles if y.name.lower() == role.lower()):
                    pingrole = r
                r = pingrole
                pingrole = discord.utils.get(ctx.message.server.roles, name=r)
                await self.bot.edit_role(ctx.message.server, pingrole, mentionable=True)
                nowpingable = await self.bot.say('```%s is now pingable for %s seconds.```' % (r, pingtime))
                await asyncio.sleep(pingtime)
                await self.bot.edit_role(ctx.message.server, pingrole, mentionable=False)
                await self.bot.delete_message(ctx.message)
                await self.bot.delete_message(nowpingable)
            else:
                print('%s failed to use ?ping %s at %s' % (ctx.message.author.name, role, datetime.datetime.now()))
                notwhitelisted = await self.bot.say('```%s is not whitelisted.```' % role)
                ctx.command.reset_cooldown(ctx)
                await asyncio.sleep(5)
                await self.bot.delete_message(ctx.message)
                await self.bot.delete_message(notwhitelisted)

    # (oh my, that's an ugly function)
    @commands.command(pass_context=True)
    @commands.has_any_role(*admin_roles)
    async def rotate(self, ctx): 
        print('----Pulling repo')
        subprocess.call(["git", "-C", repodir, "pull"]) #git pull repo
        with open(indexdir, 'r') as f: #find homepage invite from index.html
            indexhtml = f.read()
        discord_inviteURL = re.search(r'<a href="https:\/\/(discord.gg\/+[a-zA-Z0-9]+)" class="modal-link">JOIN<\/a>', indexhtml).group(1)
        discord_invitecode = discord_inviteURL.split('discord.gg/')[1]
        try:
            invite = await self.bot.get_invite(discord_inviteURL)
        except:
            print('Mistmatch between repo and current server invite.')
        await self.bot.delete_invite(invite) #await delete invite 
        message = await self.bot.send_message(ctx.message.channel, '```Rotating invite...```')
        invite = await self.bot.create_invite(self.bot.get_channel('552474543067889710'), max_age=0, unqiue=True) #create new invite
        new_indexhtml = indexhtml.replace(discord_invitecode, invite.code)
        with open(indexdir, 'w') as file: #replace invite index.html
            file.write(new_indexhtml)   
        #git push to remote
        print('----Adding changes')
        subprocess.call(["git", "-C", repodir, "add", "-u",])
        print('----Comitting')
        subprocess.call(["git", "-C", repodir, "commit", "-m", "Rotate the invite link"])
        print('----Pushing to remote')
        subprocess.call(["git", "-C", repodir, "push"])
        await self.bot.edit_message(message, '```Rotated invite.```')

def setup(bot):
    bot.add_cog(Basic(bot))
