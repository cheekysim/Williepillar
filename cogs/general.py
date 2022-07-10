from optparse import Option
import discord
from discord.ext import commands
from discord.commands import slash_command
import json

with open('config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="server", description="Shows details about the server", guild_ids=[703637471212077096])
    async def server(self, ctx):
        s = ctx.guild
        embed=discord.Embed(title="Server Information:", description="", color=0x6600ff)
        embed.set_author(name=s.name)
        #embed.set_thumbnail(url=s.icon_url_as(format="png"))
        embed.add_field(name="Server Owner", value=s.owner, inline=True)
        embed.add_field(name="Created", value=s.created_at, inline=True)
        embed.add_field(name="Created", value=s.created_at, inline=True)
        embed.set_footer(text=f"{self.bot.user.name} | Requested By: {ctx.author.mention}")
        await ctx.respond(embed=embed)

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
         await ctx.respond(f"Ping is currently: {round(self.bot.latency * 1000)}ms")

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        await ctx.respond(f"The ID of {user} is {user.id}")

def setup(bot):
    bot.add_cog(General(bot))