import discord
from discord import app_commands
from discord.ext import commands

class Say(commands.GroupCog, name="say"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    @app_commands.command(name = "goodbye")
    async def byebye(self, interaction: discord.Interaction):
        if interaction.user.id == 267672597045575691:
            await interaction.response.send_message("I'm feeling sleepy, is it time to go? Well, it was visiting you, goodbye! — <@1052310605735919646> \:)", ephemeral=True)
        else:
            await interaction.response.defer(ephemeral=True)

async def setup(bot):
    await bot.add_cog(Say(bot))