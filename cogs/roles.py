import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole

from datetime import datetime
from configparser import ConfigParser
import ast
import asyncio
import traceback
import sys

ROLES_CH = []
ROLES_MS = []
Whitelist = [] 
pingwhitelist = []
newprole = None
pingtime = 60

#region FUNCTIONS

# Parse a valid reaction roles message and return the name of the role that matches r
# A valid reaction roles message is expected to contain one or more individual lines that look like:
# :emoji: <@&ID> Brief description
# :emoji2: <@&ID2> Brief description 
# :emoji3: <@&ID3> Brief description
def rolesParser (msg, r):
    sp1 = msg.split("\n")
    ids = []
    for line in sp1:
        if r.name in line or str(r.id) in line: # To work with both unicode and custom
            ids.append(int(line.split("&")[1].split(">")[0])) # Append the role's id
    return ids # Return the list so that the module works with multiple roles per emoji

def loadConfig ():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Load config
    global ROLES_CH 
    ROLES_CH = ast.literal_eval(config_object["LISTS"]["ROLES_CH"]) #Since everything is a string
    global ROLES_MS 
    ROLES_MS= ast.literal_eval(config_object["LISTS"]["ROLES_MS"]) #Every list has to be re-interpreted
    global Whitelist 
    Whitelist = ast.literal_eval(config_object["LISTS"]["whitelist_rolename"])
    global pingwhitelist
    pingwhitelist = ast.literal_eval(config_object["LISTS"]["pingwhitelist"])
    global newprole
    newprole = int(config_object["VALUES"]["newprole"])
    return

def saveConfig ():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Update the values this cog is allowed to edit.
    lists = config_object["LISTS"]
    lists["ROLES_CH"] = str(ROLES_CH) # Everything saved to config.ini must be a string
    lists["ROLES_MS"] = str(ROLES_MS)
    lists["pingwhitelist"] = str(pingwhitelist)

    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return
#endregion

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        loadConfig()

    #region on_reaction events
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id in ROLES_CH: # If correct channel
            if payload.message_id in ROLES_MS: # If valid message
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                role_ids = rolesParser(msg.content, payload.emoji)
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                for id in role_ids:
                    role = guild.get_role(id)
                    if (role not in user.roles):
                        await user.add_roles(role)
                        continue
                    else: # Remove if they already have it
                        await user.remove_roles(role)
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id in ROLES_CH:
            if payload.message_id in ROLES_MS:
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                role_ids = rolesParser(msg.content, payload.emoji)
                guild = self.bot.get_guild(payload.guild_id)
                user = guild.get_member(payload.user_id)
                for role in role_ids:
                    await user.remove_roles(guild.get_role(role))
                return
    #endregion

    # We can no longer use "@commands.has_any_role(*Whitelist)" because the paremeter to has_any_role
    # Is given when the cog is loaded, which means it's empty, and it never updates.
    # The check of having a valid roles is now done inside the
    @commands.command(pass_context=True)
    async def roleid(self, ctx, *, rolename : str):
        """Returns the ID of a given role"""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            roles = ctx.message.guild.roles
            for role in (y for y in roles if y.name.lower() == rolename.lower()):
                print(role.name+': '+str(role.id))
                await ctx.send('```'+role.name+': '+str(role.id)+'```')

    @commands.command(pass_context=True)
    async def listroles(self, ctx):
        """Return all the roles in the server and their id"""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            roles = ctx.message.guild.roles
            for role in (y for y in roles if y.name != '@everyone'):
                print(role.name +' '+ str(role.id))

    @commands.command(pass_context=True)
    @commands.cooldown(rate=1, per=pingtime, type=commands.BucketType.user)
    async def ping(self, ctx, *, role : str):
        """Make a whitelist role pingable for 60 seconds. Cooldown default is 5 minutes."""
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
                #await ctx.message.delete()
                #await nowpingable.delete()
            else:
                print(ctx.message.author.name+' failed to use ?ping '+role+' at '+str(datetime.now()))
                notwhitelisted = await ctx.send('```'+role+' is not whitelisted.```')
                ctx.command.reset_cooldown(ctx)
                await asyncio.sleep(5)
                #await ctx.message.delete()
                #await notwhitelisted.delete()

    #region functions to edit configuration
    @commands.command()
    async def addreactionchannel(self, ctx, chn : str):
        """Add a channel to the whitelist of the role_on_reaction event."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            id = int(chn.split("#")[1].split(">")[0])
            if id not in ROLES_CH:
                ROLES_CH.append(id)
                saveConfig()
                await ctx.send("Added ["+chn+"] to the list of channels.")
        await ctx.send("The list right now is:")
        await ctx.send(ROLES_CH)

    @commands.command()
    async def addreactionmessage(self, ctx, msg : int):
        """Add a message to the whitelist of the role_on_reaction event."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            if msg not in ROLES_MS:
                ROLES_MS.append(msg)
                saveConfig()
                await ctx.send("Added ["+str(msg)+"] to the list of messages.")
        await ctx.send("The list right now is:")
        await ctx.send(ROLES_MS)

    @commands.command()
    async def removereactionchannel(self, ctx, chn : str):
        """Remove a channel from the whitelist of the role_on_reaction event."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            id = int(chn.split("#")[1].split(">")[0])
            if id in ROLES_CH:
                ROLES_CH.remove(id)
                saveConfig()
                await ctx.send("Removed ["+chn+"] from the list of messages.")
        await ctx.send("The list right now is:")
        await ctx.send(ROLES_CH)

    @commands.command()
    async def removereactionmessage(self, ctx, msg : int):
        """Remove a message from the whitelist of the role_on_reaction event."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            if msg in ROLES_MS:
                ROLES_MS.remove(msg)
                saveConfig()
                await ctx.send("Removed ["+str(msg)+"] from the list of messages.")
        await ctx.send("The list right now is:")
        await ctx.send(ROLES_MS)

    @commands.command()
    async def addpingrole(self, ctx, *, rname : str ):
        """Add a role to the whitelist of pingable roles."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            if rname not in pingwhitelist:
                pingwhitelist.append(rname)
                saveConfig()
                await ctx.send("Added ["+rname+"] to the list of pingable roles.")
        await ctx.send("The list right now is:")
        await ctx.send(pingwhitelist)

    @commands.command()
    async def removepingrole(self, ctx, *, rname : str):
        """Remove a role from the whitelist of pingable roles."""
        global Whitelist
        if not len([role for role in ctx.author.roles if role.name in Whitelist]):
            raise MissingAnyRole
        else:
            if rname in pingwhitelist:
                pingwhitelist.remove(rname)
                saveConfig()
                await ctx.send("Removed ["+rname+"] from the list of pingable roles.")
        await ctx.send("The list right now is:")
        await ctx.send(pingwhitelist)

    #@commands.command()
    #async def printdebug(self, ctx):
    #    await ctx.send("Whitelist is:")
    #    await ctx.send(Whitelist)

    #endregion


def setup(bot):
    bot.add_cog(roles(bot))