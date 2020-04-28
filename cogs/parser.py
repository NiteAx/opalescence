from discord.ext import commands
import asyncio
import re
from cogs.storage import *
from tinydb import TinyDB, Query
from pathlib import Path

parentdir = Path('../')
dbdir = str(parentdir / 'db.json')
db  = TinyDB(dbdir)  

# Move to config.py?
modrole = '175814520118312960'

def revfilter(msg): #First, a filter is constructed based on stuff
    #print('-------------------------------------------------------\nMessage: '+msg)
    if QueryCC('parser', 'template') == False:
        return False
    Templates = QueryCC('parser', 'template') # Return all templates stored by this cog.
    #print('Templates: ')
    #print(Templates)
    for template in Templates: 
        #print('Current template: '+template['value'])
        occurrences = re.findall(template['value'], msg) #Return all occurences that match template
        #print(occurrences)
        if occurrences == []:
            return False
        Exceptions = QueryCNC('parser', template['name'], 'exception') #Return all exceptions
        #print('Exceptions: ')
        #print(Exceptions)
        if Exceptions == False:
            continue
        else:
            exceptions = [Exception['value'] for Exception in Exceptions]
            #print(exceptions)
            flag = 0
            for occurrence in occurrences:
                for exception in exceptions:
                    if exception in occurrence:
                        #print(exception+' found in '+occurrence)
                        flag+=1
                    else:
                        #print(exception+' not found in '+occurrence)
                        continue
            #print(len(occurrences))
            #print(flag)
            if flag == len(occurrences):
                return False
            elif flag < len(occurrences):
                return True
                
class Parser(): #Finally, parser checks message against revfilter() and deletes if necessary 
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message): #Listen to messages
        if message.server.id == '98609319519453184': #Only listen to Manechat
          if message.author.id != '349942347905236992': #Ignore yourself
            if message.author.top_role.id != modrole: #Ignore mods
              if revfilter(message.content) == True:
                #print(message.author.top_role.id)
                #print('Deleting pleb')
                await self.bot.delete_message(message)
                await self.bot.send_message(self.bot.get_channel('141020464028844033'), '```Removed message from '+message.author.name+'#'+message.author.discriminator+' in #'+message.channel.name+':\n '+message.content+'```') #Report deletion to log channel
                  
    async def on_message_edit(self, before, after): #Listen to message edits
        if after.server.id == '98609319519453184': #Only listen to Manechat
          if after.author.id != '349942347905236992': #Ignore yourself
            if after.author.top_role.id != modrole: #Ignore mods
              if revfilter(after.content) == True:
                #print(after.author.top_role.id)
                #print('Deleting pleb')
                await self.bot.delete_message(after)
                await self.bot.send_message(self.bot.get_channel('141020464028844033'), '```Removed edited message from '+after.author.name+'#'+after.author.discriminator+' in #'+after.channel.name+':\n '+after.content+'```') #Report deletion to log channel
              
    # No createWhitelist because we can't create a whitelist without category and value
    
    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def getTemplates(self): #Returns all templates
        if QueryCC('parser', 'template') == False:
            await self.bot.say('```'+'No templates.```')
        else:
            Templates = QueryCC('parser', 'template')
            templates = [Template['value'] for Template in Templates]
            for template in Templates:
                await self.bot.say('```'+template['name']+':'+template['value']+'```')

    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def getExceptions(self): #Returns all Exceptions
        if QueryCC('parser', 'exception') == False:
            await self.bot.say('```'+'No exceptions.```')
        else:
            Templates = QueryCC('parser', 'template')
            templates = [Template['name'] for Template in Templates]
            constring = '```---Exceptions'
            for idx,template in enumerate(templates):            
                constring += '\n'+template+':'
                if QueryCNC('parser', template, 'exception'):
                    Exceptions = QueryCNC('parser', template, 'exception')
                    exceptions = [Exception['value'] for Exception in Exceptions]
                    for exception in exceptions:
                        constring += '\n'+exception
                if idx+1 <= len(templates):
                    constring += '\n'
            constring += '```'
            await self.bot.say(constring)

    @commands.group()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def deleteWhitelist(self, name : str):
        if RemoveCN('parser', name):
          await self.bot.say('```'+'Deleted '+name+' from Whitelists.```')
          return True
        await self.bot.say('```'+name+' not in Whitelists.'+'```')
        return False

    @commands.command()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def addTemplate(self, name : str, template : str, ):
        """        
        This function accepts flags, like IGNORECASE. This should be known and decided at this point for eachcase.
        The starting r'( and the finishing )' must be added by us. The special characters inside template, if any, don't need escaping.
        """
        if Insert({'cog': 'parser', 'name': name, 'category': 'template', 'value': template}): 
          await self.bot.say('```'+'Added '+template+' to '+name+'.```')
          return True
        else: 
          await self.bot.say('```'+'Unable to add template: '+template+'.```')
          return False #Failed to insert.

    # No removeTemplate because a whitelist with no template would break revfilter very badly.
        
    @commands.group()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def addException(self, name : str, exception : str):
        if QueryCN('parser', name) == False:
            #Can't add to non-existent whitelist
            await self.bot.say('```'+'Unable to add exception: '+exception+' because whitelist does not exist.```')
        else: 
            expression = exception # TO-DO: Coded like this it only allows cases where the significant term is after the template, not before or inside.
            if Insert({'cog': 'parser', 'name': name, 'category': 'exception', 'value': expression}): # TO-DO does this insertion actually work?
                await self.bot.say('```'+'Added '+exception+' to '+name+'.```')
                return True
            await self.bot.say('```'+'Unable to add exception: '+exception+'.```')
            return False 
        

    @commands.group()
    @commands.has_any_role('Cool Squad','Admin','Mods', 'Pinkie Pie')
    async def deleteException(self, name : str, exception : str):
        expression = exception # TO-DO: Coded like this it only allows cases where the significant term is after the template, not before or inside.
        if RemoveCNCV('parser', name, 'exception', expression):
          await self.bot.say('```'+'Deleted '+exception+' from '+name+'.```')
          return True
        await self.bot.say('```'+'Unable to delete '+exception+' from '+name+'.```')
        return False

def setup(bot):
    bot.add_cog(Parser(bot))