import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


def setup(bot):
    bot.add_cog(Admin(bot))