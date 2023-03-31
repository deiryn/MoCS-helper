import discord
from discord import app_commands, ui
from discord.ext import commands
from datetime import datetime


#bot = commands.Bot()
#async def getReportChannel():
#    await bot.wait_until_ready()
#    REPORT_CHANNEL = bot.get_channel(567760154825850913)
#    print(REPORT_CHANNEL)
#getReportChannel()

class Report(commands.GroupCog, name="report"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()      

    class CSIA_Report(ui.Modal, title="CSIA REPORT"):
        perpName = ui.TextInput(label="Name of the perpetrator", placeholder="username", required=True, min_length=3, max_length=40)
        sitDesc = ui.TextInput(label="Description of the violation", style=discord.TextStyle.long, placeholder="This happened on Papers...", required=True)
        time = ui.TextInput(label="Approximate time of violation", placeholder="15 minutes ago", required=True)
        proof = ui.TextInput(label="Proof of violation (ONLY LINKS)", placeholder="https://youtube.com/...", required=True)
        reporterName = ui.TextInput(label="Your name (optional)", placeholder="username", default="Anonymous", required=False) 

        async def on_submit(self, interaction: discord.Interaction):
            embed = discord.Embed(title="CS IA REPORT", color=0xFE0000)
            embed.description = "A copy of your report:"
            embed.add_field(name="Name", value=self.perpName, inline=False)
            embed.add_field(name="Description", value=self.sitDesc, inline=False)
            embed.add_field(name="Time", value=self.time, inline=False)
            embed.add_field(name="Proof", value=self.proof, inline=False)
            embed.add_field(name="Reporter's name", value=self.reporterName, inline=False)
            if str(interaction.channel.type) == "private":
                await interaction.response.send_message(embed=embed, ephemeral=False)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

            embed.description = "**\|\| NEW REPORT \|\|**"
            client = interaction.client
            REPORTS_CHANNEL = client.get_channel(1091019474477518868)
            await REPORTS_CHANNEL.send("<@&1003860471327244338>", embed=embed)
            
            #MOCS_GUILD = bot.get_guild(567760154825850911)
            #REPORT_CHANNEL = client.get_channel(941950163226857482)
            #print(REPORT_CHANNEL)
            #channel = REPORT_CHANNEL
            #await channel.send(embed=embed)

    @app_commands.command(name = "create", description="Start the CSIA report process")
    async def createreport(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Report.CSIA_Report())


async def setup(bot):
    await bot.add_cog(Report(bot))