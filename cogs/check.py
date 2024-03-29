import discord
from discord import app_commands
from discord.ext import commands
from requests import get, post
import datetime
import os
from asyncio import sleep
from itertools import chain
from operator import countOf

# i hate google part
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# i stop hating google part

async def getThumbnail(userid):
    get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=150x150&format=Png&isCircular=false')
    await sleep(0.5)
    userThumbnail = get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={userid}&size=150x150&format=Png&isCircular=false').json()
    userThumbnail = userThumbnail['data'][0]['imageUrl']
    return userThumbnail

# globals: groups #
ezicGroups = [5248163, 32390494, 32390383, 32373553]
#teutonniaGroups = [15294045, 15815549, 15635299, 15815551, 15815554, 15815556, 15822489] removed!
etgGroups = [4886107, 4886142, 4886144, 4886140, 4886147, 5150482, 5290857, 3633169]
#enemyGroups = ezicGroups + teutonniaGroups + etgGroups
enemyGroups = ezicGroups + etgGroups
bolshGroup = 991882
mainGroup = 872876
ministerialGroups = [3052496, 5217820, 5458754, 5225010, 5291387]
# globals: groups end #

#@bot.tree.command(name="check", description="Make a check on the profile. Useful for before and after CT.")
class Check(commands.GroupCog, name = "check"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name = "ct", description="Make a check on the profile. Useful for before and after CT.")
    @app_commands.choices(choice=[
        discord.app_commands.Choice(name='Link', value = 1),
        discord.app_commands.Choice(name="Nickname", value = 2)])
    async def ct(self, interaction: discord.Interaction, choice: discord.app_commands.Choice[int], user: str):
        
        userid = user.lower()
        if choice.value == 1:
            if userid.startswith("http://"):
                await interaction.response.send_message("Please use `https://`.", ephemeral=True)
                return
            elif not userid.startswith("https://www.roblox.com/users/"):
                await interaction.response.send_message("I cannot recognize this url. Please put in a link to the user profile.", ephemeral=True)
                return
            else:
                if not userid.endswith("/profile"):
                    await interaction.response.send_message("Please include `/profile` in the end of your link.", ephemeral=True)
                    return
                else:
                    lengthOfURL = len(userid)
                    userid = userid[29:lengthOfURL-8]
        else:
            request = {"usernames": [f"{userid}"], "excludeBannedUsers": True}
            getUsers = post("https://users.roblox.com/v1/usernames/users", json=request)
            if getUsers.status_code != 200:
                await interaction.response.send_message(f'Request error [HTTP {getUsers.status_code}], try again or report the problem.', ephermal=True)
                return
            elif len(getUsers.json()['data']) == 0:
                await interaction.response.send_message("User not found! Try to specify request!", ephemeral=True)
                return
            else:
                userid = getUsers.json()['data'][0]['id']

        embed = discord.Embed(title="CT CHECK:", description="Running a CT check...", color=0x8F55E5)
        embed.add_field(name="Name", value="*Loading data in...*", inline=True)
        embed.add_field(name="Account Age", value="*Loading data in...*", inline=True)
        embed.add_field(name="Enemy Groups", value="*Loading data in...*", inline=False)
        embed.add_field(name="Blacklisted", value="*Loading data in...*", inline=True)
        embed.add_field(name="Rank in Main Group:", value="*Loading data in...*", inline=True)
        #embed.set_thumbnail(url=userThumbnail)
        await interaction.response.send_message(embed=embed)

        await sleep(1)

        try:
            userGroups = get(f'https://groups.roblox.com/v2/users/{userid}/groups/roles').json()
        
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="CT CHECK:", description="ROBLOX API ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)
            return
        mainGroupRole = None
        #get rank in main group:
        try:
            if userGroups['data'] == []:
                mainGroupRole = "Foreigner"
            else:
                for item in userGroups['data']:
                    temporaryItem = item
                    if temporaryItem['group']['id'] == 872876:
                        mainGroupRole = temporaryItem['role']['name']
                        break
                    mainGroupRole = "Foreigner"
            userGroups = [value for i in userGroups['data'] for value in i.values()]
            userGroups = [sub['id'] for sub in userGroups]
            userInfo = get(f'https://users.roblox.com/v1/users/{userid}').json()
            #request thumbnail + wait 1 second
            userThumbnail = await getThumbnail(userid)
            userCreated = userInfo['created']
            userCreated = userCreated[:userCreated.find('.')]
            userCreated = datetime.datetime.strptime(userCreated, '%Y-%m-%dT%H:%M:%S')
            timeNow = datetime.datetime.now()
            userCreatedDelta = (timeNow - userCreated).days
            userName = userInfo['name']
            #enemygroups were here
            enemyGroupsCounter = userGroups + enemyGroups
            #print(groupsCounter)
            enemyCounter = 0
            for element in enemyGroups:
                if countOf(enemyGroupsCounter, element) > 1:
                    enemyCounter += 1
            #print(enemyCounter)
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="CT CHECK:", description="ALGORITHM ERROR. SECTION: API", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)
            return

        try:
            #google sheets shit
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            SPREADSHEET_ID = '14luZ0S23K4315kfAe9ESRltNFEpq7mKCbj-pxQBNnEY'
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            RANGE_NAME = 'CT Blacklists!G:G'
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_NAME).execute()
            nameValues = result.get('values', [])
            nameValues = chain(*nameValues)
            nameValues = list(nameValues)
            # remove the ctrl+f tip:
            del nameValues[1]
            # ----
            try:
                namePosition = nameValues.index(userName)
            except:
                namePosition = 0
            #print(namePosition)

            sheet = service.spreadsheets()
            RANGE_NAME = 'CT Blacklists!F:F'
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_NAME).execute()
            statusValues = result.get('values', [])
            statusValues = chain(*statusValues)
            statusValues = list(statusValues)
            lifted = statusValues[namePosition]
            #print(nameValues)
            #print(statusValues)
            #print(namePosition)
            #print(lifted)
            #google sheets shit end
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="CT CHECK:", description="GOOGLE API ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)
            return

        try:
            embed2 = discord.Embed(title="CT CHECK:", description="Running a CT check...", color=0x8F55E5)
            embed2.add_field(name="Name", value=f"{userName}", inline=True)
            embed2.add_field(name="Account Age", value=f"{(lambda: '>60 days', lambda: '__<60 DAYS__')[userCreatedDelta < 60]()}", inline=True)
            embed2.add_field(name="Enemy Groups", value=f"{(lambda: 'Clear!', lambda: '__ENEMY GROUPS DETECTED__')[enemyCounter > 0]()}", inline=False)
            embed2.add_field(name="Blacklisted", value=f"{(lambda: 'Not detected', lambda: '__BLACKLISTED__')[userName in nameValues and lifted == 'FALSE']()}", inline=True)
            if mainGroupRole == "Foreigner":
                embed2.add_field(name="Rank in Main Group:", value=f"__{mainGroupRole.upper()}__", inline=True)
            elif not mainGroupRole == "Foreigner" and not mainGroupRole == None:
                embed2.add_field(name="Rank in Main Group:", value=f"{mainGroupRole}", inline=True)
            else:
                embed2.add_field(name="Rank in Main Group:", value="NONE RETURNED (**not supposed to happen!**)", inline=True)
            embed2.set_thumbnail(url=userThumbnail)
            await interaction.edit_original_response(embed=embed2)
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="CT CHECK:", description="INTERNAL CODE ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)

    @app_commands.command(name = "ie", description = "A check that would be useful for IE to see the important info of the user before passing them.")
    @app_commands.choices(choice=[
        discord.app_commands.Choice(name='Link', value = 1),
        discord.app_commands.Choice(name="Nickname", value = 2)])
    async def ie(self, interaction: discord.Interaction, choice: discord.app_commands.Choice[int], user: str):
        
        userid = user.lower()
        if choice.value == 1:
            if userid.startswith("http://"):
                await interaction.response.send_message("Please use `https://`.", ephemeral=True)
                return
            elif not userid.startswith("https://www.roblox.com/users/"):
                await interaction.response.send_message("I cannot recognize this url. Please put in a link to the user profile.", ephemeral=True)
                return
            else:
                if not userid.endswith("/profile"):
                    await interaction.response.send_message("Please include `/profile` in the end of your link.", ephemeral=True)
                    return
                else:
                    lengthOfURL = len(userid)
                    userid = userid[29:lengthOfURL-8]
        else:
            request = {"usernames": [f"{userid}"], "excludeBannedUsers": True}
            getUsers = post("https://users.roblox.com/v1/usernames/users", json=request)
            if getUsers.status_code != 200:
                await interaction.response.send_message(f'Request error [HTTP {getUsers.status_code}], try again or report the problem.', ephermal=True)
                return
            elif len(getUsers.json()['data']) == 0:
                await interaction.response.send_message("User not found! Try to specify request!", ephemeral=True)
                return
            else:
                userid = getUsers.json()['data'][0]['id']
        
        embed = discord.Embed(title="IE CHECK:", description="Running an IE check...", color=0x8F55E5)
        embed.add_field(name="Name", value="*Loading data in...*", inline=True)
        embed.add_field(name="Account Age", value="*Loading data in...*", inline=True)
        embed.add_field(name="Enemy Groups", value="*Loading data in...*", inline=False)
        embed.add_field(name="In Main IRF group:", value="*Loading data in...*", inline=True)
        embed.add_field(name="In The Bolsheviks group:", value="*Loading data in...*", inline=True)
        embed.add_field(name="<3 ministries:", value=f"*Loading data in...*", inline=True)
        embed.add_field(name="Blacklisted", value="*Loading data in...*", inline=False)
        #embed.set_thumbnail(url=userThumbnail)
        await interaction.response.send_message(embed=embed)

        try:
            userGroups = get(f'https://groups.roblox.com/v2/users/{userid}/groups/roles').json()
            userGroups = [value for i in userGroups['data'] for value in i.values()]
            userGroups = [sub['id'] for sub in userGroups]
            userInfo = get(f'https://users.roblox.com/v1/users/{userid}').json()
            #request thumbnail + wait 3 seconds
            userThumbnail = await getThumbnail(userid)
            userCreated = userInfo['created']
            userCreated = userCreated[:userCreated.find('.')]
            userCreated = datetime.datetime.strptime(userCreated, '%Y-%m-%dT%H:%M:%S')
            timeNow = datetime.datetime.now()
            userCreatedDelta = (timeNow - userCreated).days
            userName = userInfo['name']
            #ezicGroups = [5248163, 32390494, 32390383, 32373553]
            #teutonniaGroups = [15294045, 15815549, 15635299, 15815551, 15815554, 15815556, 15822489]
            #etgGroups = [4886107, 4886142, 4886144, 4886140, 4886147, 5150482, 5290857, 3633169]
            #enemyGroups = ezicGroups + teutonniaGroups + etgGroups
            #bolshGroup = 991882
            #mainGroup = 872876
            #ministerialGroups = [3052496, 5217820, 5458754, 5225010, 5291387]
            #try:
            enemyGroupsCounter = userGroups + enemyGroups
            #print(groupsCounter)
            enemyCounter = 0
            for element in enemyGroups:
                if countOf(enemyGroupsCounter, element) > 1:
                    enemyCounter = enemyCounter + 1
        
            
            ministerialGroupsCounter = userGroups + ministerialGroups
            ministerialCounter = 0
            for element in ministerialGroups:
                if countOf(ministerialGroupsCounter, element) > 1:
                    ministerialCounter += 1
            

            if ministerialCounter > 0:
                temporaryUserGroups = get(f'https://groups.roblox.com/v2/users/{userid}/groups/roles').json()['data']
                for element in temporaryUserGroups:
                    match element['group']['id']:
                        case 3052496:
                            if element['role']['rank'] == 10:
                                ministerialCounter -= 1
                        case 5217820:
                            if element['role']['rank'] == 1 or element['role']['rank'] == 5:
                                ministerialCounter -= 1
                        case 5458754:
                            if element['role']['rank'] == 5 or element['role']['rank'] == 6 or element['role']['rank'] == 7:
                                ministerialCounter -= 1

                            

                #print(enemyCounter)
            #except Exception as e:
                #print(e)
            #    pass

            await sleep(1)
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="IE CHECK:", description="ROBLOX API ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)
            return

        try:
            #google sheets shit
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            SPREADSHEET_ID = '1zbNqUtaQyELNlJNl7kJuvcaCchFfzFxqSBU9olsuvbs'
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            service = build('sheets', 'v4', credentials=creds)

            
            # Call the Sheets API
            sheet = service.spreadsheets()
            RANGE_NAME = 'D:D'
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_NAME).execute()
            nameValues = result.get('values', [])
            nameValues = result.get('values', [])
            nameValues = chain(*nameValues)
            nameValues = list(nameValues)
            #print(nameValues)
            try:
                namePosition = nameValues.index(userName)
            except:
                namePosition = 0

            sheet = service.spreadsheets()
            RANGE_NAME = 'I:I'
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_NAME).execute()
            statusValues = result.get('values', [])
            statusValues = chain(*statusValues)
            statusValues = list(statusValues)
            lifted = statusValues[namePosition]
            #print(statusValues)
            #google sheets shit end
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="IE CHECK:", description="GOOGLE API ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)
            return

        try:
            embed = discord.Embed(title="IE CHECK:", description="Running an IE check...", color=0x8F55E5)
            embed.add_field(name="Name", value=f"{userName}", inline=True)
            embed.add_field(name="Account Age", value=f"{(lambda: '>60 days', lambda: '__<60 DAYS__')[userCreatedDelta < 60]()}", inline=True)
            embed.add_field(name="Enemy Groups", value=f"{(lambda: 'Clear!', lambda: '__ENEMY GROUPS DETECTED__')[enemyCounter > 0]()}", inline=False)
            embed.add_field(name="In Main IRF group:", value=f"{(lambda: '❌', lambda: '✅')[mainGroup in userGroups]()}", inline=True)
            embed.add_field(name="In The Bolsheviks group:", value=f"{(lambda: '❌', lambda: '✅')[bolshGroup in userGroups]()}", inline=True)
            embed.add_field(name="<3 ministries:", value=f"{(lambda: '__≥3!__', lambda: '<3')[ministerialCounter < 3]()}", inline=True)
            embed.add_field(name="Blacklisted", value=f"{(lambda: 'Not detected', lambda: '__BLACKLISTED__')[userName in nameValues and lifted == 'FALSE']()}", inline=False)
            embed.set_thumbnail(url=userThumbnail)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            embed2 = discord.Embed(title="IE CHECK:", description="INTERNAL CODE ERROR.", color=discord.Color.red)
            await interaction.edit_original_response(embed=embed2)

async def setup(bot):
	await bot.add_cog(Check(bot))
