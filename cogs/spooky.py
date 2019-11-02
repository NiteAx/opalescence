#this module is currently disabled in config
import discord
import random
import asyncio

roles = ['639240512716406789','639108166721863701']

# trrrixed:639108145674846239  tricked: 639240512716406789, treat: 639108166721863701

class Spooky():
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message): #Listen to messages
        if message.server.id == '98609319519453184': #Only listen to manechat
          if message.channel.id == '144262229691334656' or message.channel.id == '141020464028844033': #mylittlebot or sweetielog
            if message.author.id != '349942347905236992': #Ignore yourself
                if 'trick or treat' in message.content.lower():
                    print(message.author.name+' said Trick or Treat!')
                    trickrole = discord.utils.get(message.server.roles, id='639108145674846239')
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
                        if chosenrole.id == '639108166721863701':
                            await self.bot.send_message(self.bot.get_channel(message.channel.id), 'Treats!')
                        else:
                            await self.bot.send_message(self.bot.get_channel(message.channel.id), 'Tricked!')
                            await asyncio.sleep(3)
                            #await self.bot.add_roles(user, trickrole)
                            await self.bot.send_message(self.bot.get_channel('141020464028844033'), '!assignrole @Trrrixed <@'+message.author.id+'> for: 2 minutes')
                    else:
                        print('User already has role from list.')
                        await self.bot.send_message(self.bot.get_channel(message.channel.id), "You've already joined a role, silly!")
                    
def setup(bot):
    bot.add_cog(Spooky(bot))