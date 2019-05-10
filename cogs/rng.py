import random
from discord.ext import commands

class RNG():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))


def setup(bot):
    bot.add_cog(RNG(bot))