import discord
from discord.ext import commands

class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods')
    async def joined(self, member : discord.Member):
        """Says when a member joined."""
        await self.bot.say('{0.name} joined in {0.joined_at}. Such a qtpie'.format(member))

    @commands.group(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods')
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await self.bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

    @cool.command(name='bot')
    @commands.has_any_role('Cool Squad','Admin','Mods')
    async def _bot(self):
        """Is the bot cool?"""
        await self.bot.say('Yes, the bot is cool.')


def setup(bot):
    bot.add_cog(Members(bot))