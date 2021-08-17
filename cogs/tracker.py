#Keeps track of deleted messages and logs them to a logging channel in a test server
#Keeps track of reactions added and removed from messages posted since bot's last startup

from discord.ext import commands
import discord
import sys
sys.path.append('..')
from config import *
import asyncio
import random
import time
import re
import datetime
from datetime import datetime

embedflag = 0
ignoredchannels = [526339834432716815] #sweetielog
commonformat = ['.png','.jpeg','.jpg','.gif']
User_join = False

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
              print(message.author.name+" deleted: "+message.content)
        else:
          if message.guild.id == guild_id:
              if (message.channel.id not in ignoredchannels) and (message.author.id != 235088799074484224):
                  if len(message.content) == 0:   #If message has no text
                      msgcontent = message.content    #Message is empty
                  else:
                      msgcontent = ':page_facing_up:: '+message.content   #Else, message has text
                  import random
                  r = lambda: random.randint(0,255)
                  colors = ('0x%02X%02X%02X' % (r(),r(),r()))
                  embed = discord.Embed(title='Message from '+message.author.name+'#'+message.author.discriminator+' was deleted in #'+message.channel.name, description=msgcontent, color=int(colors,16)) #Create embed with Username, channel, and message content and color
                  try: #Try to attach image to embed
                      for format in commonformat:
                          if format not in message.attachments[0].proxy_url:
                              embed.description=message.attachments[0].proxy_url
                              embedflag = 1
                          else:
                              embed.set_image(url=message.attachments[0].proxy_url)
                              embedflag = 1
                  except: #If message has no attachment, search message for key strings and attach link to embed
                      if '.png' in message.content:
                          s = message.content
                          result = re.search('http(.*).png', s)
                          result = 'http'+result.group(1)+'.png'
                          embed.set_image(url=result)
                          embedflag = 1
                      elif '.jpg' in message.content:
                          s = message.content
                          result = re.search('http(.*).jpg', s)
                          result = 'http'+result.group(1)+'.jpg'
                          embed.set_image(url=result)
                          embedflag = 1
                      elif '.jpeg' in message.content:
                          s = message.content
                          result = re.search('http(.*).jpeg', s)
                          result = 'http'+result.group(1)+'.jpeg'
                          embed.set_image(url=result)
                          embedflag = 1
                      elif '.gif' in message.content:
                          s = message.content
                          result = re.search('http(.*).gif', s)
                          result = 'http'+result.group(1)+'.gif'
                          embed.set_image(url=result)
                          embedflag = 1
                      else:
                          embedflag = 0
                  if embedflag == 1: #If we have created an embed (message had image), post to #sweetielog
                      identifier = '<@'+str(message.author.id)+'>'
                      deletetime = str(datetime.utcnow()).split('.')[0]+' UTC'
                      embed.set_footer(text=deletetime+' '+identifier)
                      await self.bot.get_channel(image_channel).send(embed=embed)
                  #else: #If we don't have an embed (message contains no image), post to test server logging channel
                      #await self.bot.get_channel(message_channel).send('['+(str(message.created_at)).split('.')[0]+' UTC] #'+message.channel.name+' '+message.author.name+' ('+str(message.author.id)+')'+' : '+message.content)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.custom_emoji == True:
            message = '['+(str(datetime.now())).split('.')[0]+' UTC] '+user.name+" reacted : "+reaction.emoji.name
            print(message)
            await self.bot.get_channel(reaction_channel).send(message)
        else:
            message = '['+(str(datetime.now())).split('.')[0]+' UTC] '+user.name+" reacted : "+reaction.emoji
            print(message)
            await self.bot.get_channel(reaction_channel).send(message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.custom_emoji == True:
            message = '['+(str(datetime.now())).split('.')[0]+' UTC] '+user.name+" removed reaction : "+reaction.emoji.name
            print(message)
            await self.bot.get_channel(reaction_channel).send(message)
        else:
            message = '['+(str(datetime.now())).split('.')[0]+' UTC] '+user.name+" removed reaction : "+reaction.emoji
            print(message)
            await self.bot.get_channel(reaction_channel).send(message)

    @bot.command()
    @commands.has_any_role(*Whitelist)
    async def userjoin(ctx):
        global User_join
        User_join = not User_join
        print(User_join)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if User_join:
            await self.client.get_channel(141020464028844033).send(f"{member.mention} has joined the server. (Created {member.created_at})")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == guild_id:
            message = member.name+' ('+str(member.id)+') left the server.'
            await self.bot.get_channel(141710126628339712).send(message)

def setup(bot):
    bot.add_cog(Tracker(bot))
