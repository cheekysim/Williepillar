import inspect
import json
import os
import sys

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.ui import View

from modules.embed import embed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))


with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]


class General(commands.Cog, View):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="server", description="Shows details about the server", guild_ids=[703637471212077096])
    async def server(self, ctx):
        s = ctx.guild
        date = s.created_at
        bots = 0
        for i in s.members:
            print(i)
            if i.bot:
                bots += 1
        await ctx.respond(
            embed=embed(ctx, title="Server Information:", thumbnail=s.icon, author=[{'name': s.name, 'icon': s.icon}],
                        fields=[
                            {'name': 'ID', 'value': s.id, 'inline': True},
                            {'name': 'Server Owner', 'value': s.owner, 'inline': True},
                            {'name': 'Description', 'value': s.description, 'inline': True},
                            {'name': 'Channels',
                             'value': f'{len(s.text_channels)} Text | {len(s.voice_channels)} Voice', 'inline': True},
                            {'name': 'Members', 'value': s.member_count, 'inline': True},
                            {'name': 'Humans', 'value': s.member_count - bots, 'inline': True},
                            {'name': 'Bots', 'value': bots, 'inline': True},
                            {'name': 'Verification', 'value': s.verification_level, 'inline': True},
                            {'name': 'Created',
                             'value': f'{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}',
                             'inline': True}
                        ]))

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
        await ctx.respond(embed=embed(ctx, title=f"Ping is currently: {round(self.bot.latency * 1000)}ms"))

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        user = user or ctx.author
        await ctx.respond(embed=embed(ctx, title=f"{user.name}'s id is {user.id}"))

    @slash_command(name="image", guild_ids=[703637471212077096])
    async def image(self, ctx):
        await ctx.respond(embed=embed(ctx, type="image", url=ctx.guild.icon))


def setup(bot):
    bot.add_cog(General(bot))
