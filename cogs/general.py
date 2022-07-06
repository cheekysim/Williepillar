import discord
from discord.ext import commands
from discord_slash import cog_ext
import json
import os

with open('Williepillar/config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="Server", description="Shows details about the server", guild_ids=guild_ids)
    async def server(self, ctx):
        s = ctx.guild
        embed=discord.Embed(title="Server Information:", description="", color=0x6600ff)
        embed.set_author(name=s.name, icon_url=s.icon_url_as(format="png"))
        embed.set_thumbnail(url=s.icon_url_as(format="png"))
        embed.add_field(name="Server Owner", value=s.owner, inline=True)
        embed.add_field(name="Created", value=s.created_at, inline=True)
        embed.add_field(name="Created", value=s.created_at, inline=True)
        embed.set_footer(text=f"{self.bot.user.name} | Requested By: {ctx.author.mention}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))