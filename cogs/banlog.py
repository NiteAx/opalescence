import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import sys
sys.path.append('..')
from config import *

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

parentdir = Path('../')
dbdir = str(parentdir / 'client_secret.json')
credentials = ServiceAccountCredentials.from_json_keyfile_name(dbdir, scope)
gc = gspread.authorize(credentials)
wks = gc.open("Manechat AiO")
wks = wks.worksheet("Form Responses 1")

class Banlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*Whitelist)
    async def banlog(self, ctx, userID : str):
        print(userID)
        if len(userID) <= 18 and userID.isdigit() == False:
            await ctx.send('```Invalid input.```')
            raise ValueError('Invalid input')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(dbdir, scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("Manechat AiO")
        wks = wks.worksheet("Form Responses 1")
        results = (wks.findall(userID))
        if len(results) == 0:
            await ctx.send('```No results returned for user.```')
            raise IndexError('Length of results is 0.')
        userRow = list(reversed(results))[0].row
        userCol = list(reversed(results))[0].col
        uname = wks.cell(userRow,userCol-1).value
        count = len(results)
        warnings = silences = bans = 0
        for case in reversed(results):
            title = wks.cell(case.row, 2).value
            if title == "Warning":
                warnings = warnings+1
            elif title == "Silence":
                silences = silences+1
            elif title == "Ban":
                bans = bans+1
        await ctx.send('``` ['+uname+'] Warnings: '+str(warnings)+' Silences: '+str(silences)+' Bans: '+str(bans)+'```')
        warnings = silences = bans = 0
        for case in reversed(results):
            if (case.col==4) or (case.col==10) or (case.col==17):
                title = wks.cell(case.row, 2).value
                if title == "Warning":
                    stop = 4
                else:
                    stop = 5
                report = wks.range(case.row,(case.col-1),case.row,case.col+stop)
                user = report[0].value
                userID = report[1].value
                offense = report[2].value
                addinfo = report[3].value
                if title == "Warning":
                    date = report[4].value
                    reportedBy = report[5].value
                else:
                    duration = report[4].value
                    date = report[5].value
                    reportedBy = report[6].value
                #print(title)
                #print(user+" "+userID)
                #print(date+" "+offense)
                #print(duration+" "+addinfo)
                #print("------------------------------------")
                if title == "Warning":
                    await ctx.send('['+title+'] '+date+' - '+offense+' | '+addinfo)
                else:
                    await ctx.send('['+title+'] ('+duration+') '+date+' - '+offense+' | '+addinfo)
            else:
                await ctx.send('```Invalid input.```')
                break

def setup(bot):
    bot.add_cog(Banlog(bot))
