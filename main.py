from discord.ext import commands
from os import listdir
from os.path import isfile, join
import sys
sys.path.append('..')
from config import *
import traceback

cogs_dir = "cogs"

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def unload(extension_name : str):
    module = bot.extensions.get(extension_name)
    if module is None:
        await bot.say("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
        return
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))
    
@bot.command()
@commands.has_any_role('Cool Squad','Admin','Mods')
async def reload(extension_name : str):
    module = bot.extensions.get(extension_name)
    if module is None:
        await bot.say("```py\n"+"ModuleNotFoundError: No module named '"+extension_name+"'\n```")
        return
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    #await bot.say("{} unloaded.".format(extension_name))
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} reloaded.".format(extension_name))
    
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
                traceback.print_exc()
    print("Loaded: "+(' '.join(extensionss)))
    
    while True:
        try:
            bot.run(token)
        except ConnectionResetError:
            traceback.print_exc()
            continue
    
