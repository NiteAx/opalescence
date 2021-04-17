from discord.ext import commands
import discord
from discord.utils import get
import sys
sys.path.append('..')
from config import *

# Coming soon.

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


def setup(bot):
    bot.add_cog(events(bot))