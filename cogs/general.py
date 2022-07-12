import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
from discord.ui import Button, View
import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed


with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]

class MyView(View):
    @discord.ui.button(label="Check", style=discord.ButtonStyle.red)
    async def button_callback(self,button, interaction):
        button.label = "it works"
        button.disabled
        await interaction.response.send_message("it works")
    @discord.ui.button(label="Check2", style=discord.ButtonStyle.blurple)
    async def button_callback2(self,button, interaction):
        await interaction.response.send_message("it works2")
    @discord.ui.button(label="Hi", style=discord.ButtonStyle.blurple)
    async def button_callback2(self,button, interaction):
        await interaction.response.send_message("Hi cheeky")


class General(commands.Cog,View):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="server", description="Shows details about the server", guild_ids=[703637471212077096])
    async def server(self, ctx):
        s = ctx.guild
        date = s.created_at
        await ctx.respond(embed=embed(self, ctx, title="Server Information:", thumbnail=s.icon, author=[{'name':s.name,'icon':s.icon}], fields=[
            {'name':'ID','value':s.id,'inline':True},
            {'name':'Server Owner','value':s.owner,'inline':True}, 
            {'name':'Description','value':s.description,'inline':True},
            {'name':'Channels','value':'todo','inline':True},
            {'name':'Members','value':s.member_count,'inline':True},
            {'name':'Humans','value':'todo','inline':True},
            {'name':'Bots','value':'todo','inline':True},
            {'name':'Verifiction','value':s.verification_level,'inline':True},
            {'name':'Created','value':f'{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}','inline':True}
            ]))

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
         await ctx.respond(embed=embed(self, ctx, title=f"Ping is currently: {round(self.bot.latency * 1000)}ms"))

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(embed=embed(self, ctx, title=f"{user.name}'s id is {user.id}"))
    
    @slash_command(name="image", guild_ids=[703637471212077096])
    async def image(self, ctx):
        await ctx.respond(embed=embed(self, ctx, type="image",url=ctx.guild.icon))
        
    @slash_command(name="button", guild_ids=[703637471212077096])
    async def button(self,ctx):
        button = Button(label="Youtube",url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        button1 = Button(label="Hi",style=discord.ButtonStyle.blurple)
        async def button_callback(self,button, interaction):
            await interaction.response.send_message("Hi cheeky")
        button.callback = button_callback
        view = MyView()
        view.add_item(button1)
        view.add_item(button)
        await ctx.respond(view = view)


def setup(bot):
    bot.add_cog(General(bot))