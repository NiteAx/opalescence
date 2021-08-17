import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole

from datetime import datetime
from configparser import ConfigParser
import ast
import asyncio
import traceback
import sys
import random

Event_roles = []
Whitelist = []
Rarity = False
RD = False

#region FUNCTIONS

def loadConfig ():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Load config
    global Whitelist 
    Whitelist = ast.literal_eval(config_object["LISTS"]["whitelist_rolename"])
    return
#endregion

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        loadConfig()

    @commands.command(pass_context=True)
    async def startevent(self, ctx, *, event : str):
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            if "rd" in event or "rainbow dash" in event:
                global RD
                RD = True
            if "rarity" in event:
                global Rarity
                Rarity = True

    @commands.command(pass_context=True)
    async def endevent(self, ctx):
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            global RD
            global Rarity
            RD = Rarity = False
            
            global Event_roles
            for r in Event_roles:
                role = discord.utils.get(ctx.guild.roles, id=r)
                await role.delete()
            Event_roles = []

    @commands.command(pass_context=True)
    async def addeventrole(self, ctx, *, role : int): # For Rainbow Dash Day
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            global Event_roles
            Event_roles.append(role)

    @commands.command(pass_context=True)
    async def joinrole(self, ctx):
        global Event_roles
        if RD:
            user = ctx.message.author
            memberoles = []
            for role in user.roles:
                memberoles.append(role.id)
            if set(Event_roles).isdisjoint(set(memberoles)):
                chosenrole = ctx.message.guild.get_role(random.choice(Event_roles))
                print('Random Role: '+chosenrole.name+' '+str(chosenrole.id))
                await user.add_roles(chosenrole)
        if Rarity:
            user = ctx.message.author
            memberoles = []
            for role in user.roles:
                memberoles.append(role.id)
            if set(Event_roles).isdisjoint(set(memberoles)):
                with open("clothes.txt", "r") as file:
                    allText = file.read()
                    clothes = list(map(str, allText.split()))
                    cloth = random.choice(clothes)
                with open("adjectives.txt", "r") as file:
                    allText = file.read()
                    adjectives = list(map(str, allText.split()))
                    adjective = random.choice(adjectives)
                rolename = adjective+" "+cloth
                color = random.randint(0, 0xFFFFFF)
                
                await ctx.guild.create_role(name=rolename, colour=discord.Colour(color))
                role = discord.utils.get(ctx.guild.roles, name=rolename)
                Event_roles.append(role.id)
                user = ctx.message.author
                await user.add_roles(role)



def setup(bot):
    bot.add_cog(events(bot))