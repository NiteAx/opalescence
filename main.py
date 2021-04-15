import discord
from discord.ext import commands
import asyncio

from os import listdir
from os.path import isfile, join
import sys
sys.path.append('..')
from config import *

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.guild_messages = True
intents.guild_reactions = True
bot = commands.Bot(command_prefix='?', intents=intents)

cogs_dir = "cogs"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.loop.create_task(status_task())

@bot.command()
@commands.has_any_role(*Whitelist)
async def load(ctx, extension_name : str):
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
    module = bot.extensions.get(extension_name)
    if module is None:
        await ctx.send("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
        return
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@bot.command()
@commands.has_any_role(*Whitelist)
async def reload(ctx, extension_name : str):
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

async def status_task():
    while True:
        manechat = bot.get_guild(98609319519453184)
        status1 = discord.Game('with '+str(manechat.member_count)+' ponies')
        await bot.change_presence(activity=status1)
        await asyncio.sleep(10)

if __name__ == "__main__":
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
