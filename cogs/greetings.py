import discord
from discord.ext import commands
from discord.commands import slash_command
import json

with open('config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.respond(f"Welcome {member.mention}!")

    @slash_command(name="hello", description="Says Hello", guild_ids=[703637471212077096])
    async def hello(self, ctx):
        await ctx.respond(f"Hello {ctx.author.name}!")

    @slash_command(name="goodbye", description="Says Goodbye", guild_ids=[703637471212077096])
    async def goodbye(self, ctx):
        await ctx.respond(f"Goodbye {ctx.author.name}!")

def setup(bot):
    bot.add_cog(Greetings(bot))