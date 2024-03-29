import json

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.ui import View

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

# It's loading the config.json file and assigning the values to the variables.
with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]


class General(commands.Cog, View):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="server", description="Shows details about the server", guild_ids=[703637471212077096])
    async def server(self, ctx):
        """
        It sends an embed with information about the server.

        :param ctx: The context of the command
        """
        s = ctx.guild
        date = s.created_at
        bots = len([i for i in s.members if i.bot])
        await ctx.respond(
            embed=embed(ctx, title="Server Information:", thumbnail=s.icon, author=[{'name': s.name, 'icon': s.icon}],
                        fields=[
                            {'name': 'ID', 'value': s.id, 'inline': True},
                            {'name': 'Server Owner', 'value': s.owner, 'inline': True},
                            {'name': 'Description', 'value': s.description, 'inline': True},
                            {'name': 'Channels', 'value': f'{len(s.text_channels)} Text | {len(s.voice_channels)} Voice', 'inline': True},
                            {'name': 'Members', 'value': s.member_count, 'inline': True},
                            {'name': 'Humans', 'value': s.member_count - bots, 'inline': True},
                            {'name': 'Bots', 'value': bots, 'inline': True},
                            {'name': 'Verification', 'value': s.verification_level, 'inline': True},
                            {'name': 'Created', 'value': f'{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}', 'inline': True}]))

    @slash_command(name="ping", description="Shows Ping", guild_ids=[703637471212077096])
    async def ping(self, ctx):
        """
        It sends a message in the channel the command was used in containing the bots latency.

        :param ctx: The context of the command
        """
        await ctx.respond(embed=embed(ctx, title=f"Ping is currently: {round(self.bot.latency * 1000)}ms"))

    @slash_command(name="id", description="Get id of user", guild_ids=[703637471212077096])
    async def id(self, ctx, user: Option(discord.User, "User", required=False)):
        """
        It gets the user's id

        :param ctx: The context of the command
        :param user: Option(discord.User, "User", required=False)
        :type user: Option(discord.User, "User", required=False)
        """
        user = user or ctx.author
        await ctx.respond(embed=embed(ctx, title=f"{user.name}'s id is {user.id}"))


def setup(bot):
    bot.add_cog(General(bot))
