from os import listdir
from os.path import isfile, join, abspath
import traceback

from discord.ext import commands

# Config is private
import sys
sys.path.append(abspath('..'))
from config import *
from common import *

cogs_dir = "cogs"

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def _load(ext : str):
    """Internal: loads module.
    :return: (success:bool, error:str)
    """
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        return False, "```py\n%s: %s\n```" % (type(e).__name__, e)
    return True, "{} loaded.".format(extension_name)

def _unload(ext : str):
    """Internal: unloads module.
    :return: (success:bool, error:str)
    """
    module = bot.extensions.get(extension_name)
    if module is None:
        return False, "```py\nModuleNotFoundError: No module named '%s'\n```" % extension_name
    bot.unload_extension(extension_name)
    return True, "{} unloaded.".format(extension_name)

@bot.command()
@commands.has_any_role(*admin_roles)
async def load(extension_name : str):
    """Loads an extension."""
    success, log = _load(extension_name)
    await bot.say(log)

@bot.command()
@commands.has_any_role(*admin_roles)
async def unload(extension_name : str):
    """Unloads an extension."""
    success, log = _unload(extension_name)
    await bot.say(log)
    
@bot.command()
@commands.has_any_role(*admin_roles)
async def reload(extension_name : str):
    """Reloads an extension."""
    # Unload
    success, log = _unload(extension_name)
    if not success:
        await bot.say(log)
        return
    # Load
    success, log = _load(extension_name)
    if not success:
        await bot.say(log)
        return
    await bot.say("{} reloaded.".format(extension_name))
    
if __name__ == "__main__":
    extensions = []
    for ext in (f.replace('.py', '') for f in glob.glob("%s/*.py" % cogs_dir)):
        if ext not in ignoredmodules:
            if _load(ext)[0]:
                extensions.append(ext)
    print("Loaded: "+(' '.join(extensions)))
    
    while True:
        try:
            bot.run(token)
        except:
            traceback.print_exc()
            pass
