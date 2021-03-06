import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import MissingAnyRole

from configparser import ConfigParser

from os import listdir
from os.path import isfile, join
import sys
import ast
import datetime
from datetime import datetime

# Cogs affected by config.ini, and so need to be reload when Whitelist changes
cogsList = ['cogs.roles']
cogs_dir = "cogs"
ignoredmodules = []
Whitelist = ['Admin', 'Mods'] # In case there is no config.ini, Admins and Mods will have priviledge by default
token = None

intents = discord.Intents.default()
intents.members=True
intents.guilds=True
intents.guild_messages=True
intents.guild_reactions=True
intents.members=True
intents.presences=True
bot = commands.Bot(command_prefix='?', intents=intents)

#region Config functions.
def loadConfig ():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Load config
    global Whitelist
    Whitelist = ast.literal_eval(config_object["LISTS"]["whitelist_rolename"]) #Since everything is a string
    global ignoredmodules
    ignoredmodules = ast.literal_eval(config_object["LISTS"]["ignoredmodules"]) #Every list has to be re-interpreted
    global token
    token = config_object["VALUES"]["token"]
    return

def saveConfig ():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    #Update the values this cog is allowed to edit.
    lists = config_object["LISTS"]
    lists["whitelist_rolename"] = str(Whitelist) # Everything saved to config.ini must be a string

    #Write changes back to file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return
#endregion

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.get_channel(141020464028844033).send("```Restarted at: "+(str(datetime.now())).split('.')[0]+' UTC '+"```")
    bot.loop.create_task(status_task())

@bot.command()
@commands.has_any_role(*Whitelist)
async def load(ctx, extension_name : str):
    global Whitelist
    if not len([role for role in ctx.author.roles if role.name in Whitelist]):
        raise MissingAnyRole
    else:
        """Loads an extension."""
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

@bot.command()
@commands.has_any_role(*Whitelist)
async def unload(ctx, extension_name : str):
    global Whitelist
    if not len([role for role in ctx.author.roles if role.name in Whitelist]):
        raise MissingAnyRole
    else:
        module = bot.extensions.get(extension_name)
        if module is None:
            await ctx.send("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
            return
        """Unloads an extension."""
        bot.unload_extension(extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

@bot.command()
async def reload(ctx, extension_name : str):
    global Whitelist
    if not len([role for role in ctx.author.roles if role.name in Whitelist]):
        raise MissingAnyRole
    else:
        module = bot.extensions.get(extension_name)
        if module is None:
            await ctx.send("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
            return
        """Unloads an extension."""
        bot.unload_extension(extension_name)
        """Loads an extension."""
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(extension_name))

@bot.command()
async def reloadCogs(ctx):
    global cogsList
    for cogname in cogsList:
        bot.unload_extension(cogname)
        try:
            bot.load_extension(cogname)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(cogname))

@bot.command()
async def addmodrole(ctx, *, rname : str ):
    """Add a role to the whitelist of privileged roles."""
    global Whitelist
    if not len([role for role in ctx.author.roles if role.name in Whitelist]):
        raise MissingAnyRole
    else:
        if rname not in Whitelist:
            Whitelist.append(rname)
            saveConfig()
            await reloadCogs(ctx)
            await ctx.send("Added ["+rname+"] to the list of priviledged roles.")

@bot.command()
async def removemodrole(ctx, *, rname : str ):
    """Remove a role from the whitelist of privileged roles."""
    global Whitelist
    if not len([role for role in ctx.author.roles if role.name in Whitelist]):
        raise MissingAnyRole
    else:
        if rname in Whitelist:
            Whitelist.remove(rname)
            saveConfig()
            await reloadCogs(ctx)
            await ctx.send("Removed ["+rname+"] from the list of priviledged roles.")

async def status_task():
    while True:
        manechat = bot.get_guild(98609319519453184)
        status1 = discord.Game('with '+str(manechat.member_count)+' ponies')
        await bot.change_presence(activity=status1)
        await asyncio.sleep(10)

if __name__ == "__main__":
    loadConfig()

    extensionss = []
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        extensionss.append(extension)
        if extension in ignoredmodules:
            extensionss.pop()
            continue
        else:
            try:
                bot.load_extension(cogs_dir + "." + extension)
            except Exception as e:
                print('Failed to load extension {extension}.'.format(extension))
    print("Loaded: "+(' '.join(extensionss)))

bot.run(token)
