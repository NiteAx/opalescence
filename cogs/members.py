import discord
from discord.ext import commands

import sys
sys.path.append(abspath('..'))  # common.py
from common import *

class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*admin_roles)
    async def joined(self, member : discord.Member):
        """Says when a member joined."""
        await self.bot.say('{0.name} joined in {0.joined_at}. Such a qtpie'.format(member))

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a user is cool.
        """
        if ctx.invoked_subcommand is None:
            if has_any_role(ctx.message.author, admin_roles):
                await self.bot.say('Yes, %s is quite cool.' % ctx.message.author.display_name)
            else:
                await self.bot.say('No, %s is not cool' % ctx.message.author.display_name)

    # Oh look ! a subcommand (will overwrite the above one)
    # --> matches '?cool bot' only
    @cool.command(name='bot')
    @commands.has_any_role(*admin_roles)
    async def _bot(self):
        """Is the bot cool?"""
        await self.bot.say('Yes, the bot is cool.')


def setup(bot):
    bot.add_cog(Members(bot))
