import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from modules.embed import embed
from datetime import datetime
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
        date = s.created_at
        await ctx.respond(embed=embed(title="Server Information:", color=0x6600ff, author=[{'name':s.name}], fields=[{'name':'Server Owner','value':s.owner,'inline':True}, {'name':'Created','value':f'{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}','inline':True}], footer=[{'text':f'{self.bot.user.name} | Requested By: {ctx.author.name}'}]))

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
         await ctx.respond(f"Ping is currently: {round(self.bot.latency * 1000)}ms")

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(embed=embed(title=f"{user.name}'s id is {user.id}"))


def setup(bot):
    bot.add_cog(General(bot))