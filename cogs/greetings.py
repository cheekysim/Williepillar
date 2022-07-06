import discord
from discord.ext import commands
from discord_slash import cog_ext
import json
import os

with open('Williepillar/config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome {member.mention}!")

    @cog_ext.cog_slash(name="Hello", description="Says Hello", guild_ids=guild_ids)
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")

    @cog_ext.cog_slash(name="Goodbye", description="Says Goodbye", guild_ids=guild_ids)
    async def goodbye(self, ctx):
        await ctx.send(f"Goodbye {ctx.author.name}!")

def setup(bot):
    bot.add_cog(Greetings(bot))