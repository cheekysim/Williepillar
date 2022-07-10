import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from modules.embed import embed
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
        await ctx.respond(embed=embed(title="Server Information:", color=0x6600ff, thumbnail=s.icon, author=[{'name':s.name,'icon':s.icon}], fields=[
            {'name':'ID','value':s.id,'inline':True},
            {'name':'Server Owner','value':s.owner,'inline':True}, 
            {'name':'Description','value':s.description,'inline':True},
            {'name':'Channels','value':'todo','inline':True},
            {'name':'Members','value':s.member_count,'inline':True},
            {'name':'Humans','value':'todo','inline':True},
            {'name':'Bots','value':'todo','inline':True},
            {'name':'Verifiction','value':s.verification_level,'inline':True},
            {'name':'Created','value':f'{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}','inline':True}
            ], footer=[{'text':f'{self.bot.user.name} | Requested By: {ctx.author.name}'}]))

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
         await ctx.respond(f"Ping is currently: {round(self.bot.latency * 1000)}ms")

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(embed=embed(title=f"{user.name}'s id is {user.id}"))
    
    @slash_command(name="image", guild_ids=[703637471212077096])
    async def image(self, ctx):
        await ctx.respond(embed=embed(type="image",url=ctx.guild.icon))


def setup(bot):
    bot.add_cog(General(bot))