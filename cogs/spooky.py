import discord
import random
import asyncio

roles = ['638752293541511199','638752350542102560']

# trick: 638752293541511199, treat: 638752350542102560

class Spooky():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message): #Listen to messages
        if message.server.id == '349941841862459413': #Only listen to test server
          if message.channel.id == '638752113370988575': #Trick Or Treat (test server)
            if message.author.id != '349942347905236992': #Ignore yourself
                if 'trick or treat' in message.content:
                    print(message.author.name+' said Trick or Treat!')
                    chosenrole = discord.utils.get(message.server.roles, id=random.choice(roles))
                    print('Random Role: '+chosenrole.name+' '+chosenrole.id)
                    user = message.author
                    memberoles = []
                    for role in user.roles:
                        memberoles.append(role.id)
                    #print("Member Role ID's:")
                    print(memberoles)
                    if set(roles).isdisjoint(set(memberoles)):
                        await self.bot.add_roles(user, chosenrole)
                        print('Assigning role....')
                        if chosenrole.id == '638752350542102560':
                            await self.bot.send_message(self.bot.get_channel('638752113370988575'), 'Treats!')
                        else:
                            await self.bot.send_message(self.bot.get_channel('638752113370988575'), 'Tricked!')
                            await asyncio.sleep(3)
                            await self.bot.send_message(self.bot.get_channel('638752113370988575'), '!banish <@'+message.author.id+'> for: 2 minutes')
                    else:
                        print('User already has role from list.')
                        await self.bot.send_message(self.bot.get_channel('638752113370988575'), 'F off with ur bs m8')
                    #Post message "Treats!"/"Tricked!", delay, assign role, moon command
                    
def setup(bot):
    bot.add_cog(Spooky(bot))