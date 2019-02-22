from discord.ext import commands
import discord
import sys
sys.path.append('..')
from config import *
import asyncio
import random
import time
import re
from datetime import datetime

embedflag = 0
ignoredchannels = ['526339834432716815','368960769074921472','217569473698201601','124636360437923840']
commonformat = ['.png','.jpeg','.jpg','.gif']

class Tracker():
    def __init__(self, bot):
        self.bot = bot

    """
    async def on_ready(self):
        print('Tracking!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        print('------')
    """
        
    """
    async def on_message(self, message):
        print(message.author.name+" : "+message.content)
        counter = 0
        async for msg in self.bot.logs_from(message.channel, limit=500):
            if msg.author == message.author:
                counter += 1
        print(message.author.name+" : "+str(counter))        
    """
    """
    async def on_message(self, message):
        for user in message.mentions:
            if user.id == '349942347905236992':
                print("Meow! Who called me?")
                await self.bot.send_message(message.channel,"Meow." or "Meow!")
                time.sleep(60)
    """
    async def on_message_delete(self, message):
        if message.server.id == '98609319519453184':
            if message.channel.id not in ignoredchannels:
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
                        if format not in message.attachments[0]['proxy_url']:
                            embed.description=message.attachments[0]['proxy_url']
                            embedflag = 1
                        else:
                      
                            embed.set_image(url=message.attachments[0]['proxy_url'])
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
                if embedflag == 1:
                    identifier = '<@'+message.author.id+'>'
                    deletetime = str(datetime.utcnow()).split('.')[0]+' UTC'
                    embed.set_footer(text=deletetime+' '+identifier)        
                    await self.bot.send_message(self.bot.get_channel('141020464028844033'), embed=embed)
                else:
                    await self.bot.send_message(self.bot.get_channel('349945916779921408'), '['+(str(message.timestamp)).split('.')[0]+' UTC'+'] #'+message.channel.name+' '+message.author.name+' : '+message.content)
                
    async def on_reaction_add(self, reaction, user):
        if reaction.custom_emoji == True:
            print(user.name+" reacted : "+reaction.emoji.name)
        else:
            print(user.name+" reacted : "+reaction.emoji)
    
    async def on_reaction_remove(self, reaction, user):
        if reaction.custom_emoji == True:
            print(user.name+" removed reaction : "+reaction.emoji.name)
        else:
            print(user.name+" removed reaction : "+reaction.emoji)
    """
    @commands.command(pass_context=True)
    @commands.has_any_role('Cool Squad','Admin','Mods')
    async def count(self, ctx):        
        print(ctx.message.author.name+" : "+ctx.message.content)
        print(ctx.message.channel.name)
        counter = 0
        async for msg in self.bot.logs_from(ctx.message.channel, limit=10000):
            if msg.author == ctx.message.author:
                counter += 1
            #print(msg.content)
        print(counter)
        await self.bot.say("```You have posted "+str(counter)+" messages in the past 10000 messages in this channel.```")    
    """
def setup(bot):
    bot.add_cog(Tracker(bot))