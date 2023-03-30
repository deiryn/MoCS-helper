import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
from datetime import datetime

class Report(commands.GroupCog, name="report"):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    class IAReport(ui.Modal, title="CSIA REPORT"):
        name = ui.TextInput(label="Name of the perpetrator", style=discord.TextStyle.short, placeholder="username", required=True)
        description = ui.TextInput(label="Description of the violation", style=discord.TextStyle.long, placeholder="This happened on papers...", required=True)
        time = ui.TextInput(label="Approximate time of the violation (if known)", style=discord.TextStyle.short, placeholder="15 minutes ago", required=True)
        proof = ui.TextInput(label="Proof (LINKS ONLY)", style=discord.TextStyle.short, placeholder="links to images/videos", required=True)
        yourName = ui.TextInput(label="Your name (optional)", style=discord.TextStyle.short, placeholder="username", required=False, default="Anonymous")
    
        async def on_submit(self, interaction: discord.Interaction, bot: commands.Bot):
            embedResponse = discord.Embed(title="CS IA REPORT", description="This is a copy of the report you've sent", color=0xFE0000)
            embedResponse.add_field(name="Name", value=self.name, inline=False)
            embedResponse.add_field(name="Description", value=self.description, inline=False)
            embedResponse.add_field(name="Time", value=self.time, inline=False)
            embedResponse.add_field(name="Proof", value=self.proof, inline=False)
            embedResponse.add_field(name="Reporter name provided", value=self.yourName, inline=False)
            embedResponse.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embedResponse, ephemeral=True)
            embedResponse.description = "New report logged:"
            try:
                MOCS_GUILD = bot.get_guild(705548936529575998)
                loggingChannel = discord.utils.get(MOCS_GUILD.channels, id=1091019474477518868)
            except Exception as e:
                 print(e)
            await loggingChannel.send("<@&1003860471327244338>", embed=embedResponse)

    @app_commands.command(name = "create", description="Start the MoCS IA report process.")
    async def createreport(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Report.IAReport())


async def setup(bot):
	await bot.add_cog(Report(bot))