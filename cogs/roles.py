import discord
import traceback
import sys
from discord.ext import commands
import sys
sys.path.append('..')
from config import Whitelist

ROLES_CH = []
ROLES_MS = []

# Parse a valid reaction roles message and return the name of the role that matches r
# A valid reaction roles message is expected to contain one or more individual lines that look like:
# :emoji: <@&ID> Brief description
# :emoji2: <@&ID2> Brief description 
# :emoji3: <@&ID3> Brief description

def rolesParser (msg, r):
    sp1 = msg.split("\n")
    for line in sp1:
        if r.name in line or str(r.id) in line: # To work with both unicode and custom
            return int(line.split("&")[1].split(">")[0]) # Return the role's id

def saveChannels ():
    with open("roles_ch.txt", "w") as f:
        for c in ROLES_CH:
            f.write(str(c) +"\n")
    return

def saveMessages ():
    with open("roles_ms.txt", "w") as f:
        for m in ROLES_MS:
            f.write(str(m) +"\n")
    return

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        try:
            with open("roles_ms.txt", "r") as f:
                for line in f:
                    ROLES_MS.append(int(line.strip()))
        except:
            print("File roles_ms.txt doesn't exist yet")
        try:
            with open("roles_ch.txt", "r") as f:
                for line in f:
                    ROLES_CH.append(int(line.strip()))
        except:
            print("File roles_ch.txt doesn't exist yet")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id in ROLES_CH: # If correct channel
            if payload.message_id in ROLES_MS: # If valid message
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                role_id = rolesParser(msg.content, payload.emoji)
                if role_id:
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(role_id) # Returns None for some reason?
                    await guild.get_member(payload.user_id).add_roles(role)
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id in ROLES_CH:
            if payload.message_id in ROLES_MS:
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                role_id = rolesParser(msg.content, payload.emoji)
                if role_id:
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(role_id)
                    await guild.get_member(payload.user_id).remove_roles(role)
                return

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def addreactionchannel(self, ctx, chn : str):
        id = int(chn.split("#")[1].split(">")[0])
        if id not in ROLES_CH:
            ROLES_CH.append(id)
            print(ROLES_CH)
            saveChannels()


    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def addreactionmessage(self, ctx, msg : int):
        if msg not in ROLES_MS:
            ROLES_MS.append(msg)
            print(ROLES_MS)
            saveMessages()

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def removereactionchannel(self, ctx, chn : str):
        id = int(chn.split("#")[1].split(">")[0])
        if id in ROLES_CH:
            ROLES_CH.remove(id)
            saveChannels()


    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def removereactionmessage(self, ctx, msg : int):
        if msg in ROLES_MS:
            ROLES_MS.remove(msg)
            saveMessages()



def setup(bot):
    bot.add_cog(roles(bot))