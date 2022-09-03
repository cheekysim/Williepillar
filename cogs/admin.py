
import json
import asyncio
import discord
from discord import default_permissions
from discord.commands import slash_command, Option
from discord.ext import commands
import time

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]


async def durationConverter(args):
    amount = args[:-1]
    unit = args[-1]
    multiplier = {'s': 1, 'm': 60, 'h': 3600}

    if amount.isdigit() and unit in ['s', 'm', 'h']:
        return [int(amount), unit, multiplier]

    raise commands.BadArgument()


async def timeConverter(args: int):
    if args >= 3600:
        ftime = time.strftime('%Hh %Mm %Ss', time.gmtime(args)).replace(' 0', ' ')
    elif args >= 60:
        ftime = time.strftime('%Mm %Ss', time.gmtime(args)).replace(' 0', ' ')
    else:
        ftime = args + "s"
    return ftime


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="mute", description="Mutes User", guild_ids=[703637471212077096])
    @default_permissions(moderate_members=True)
    async def mute(self, ctx: discord.ApplicationContext, user: Option(discord.User, "User", required=True), reason: Option(str, "Reason", required=True), duration: Option(str, "Duration", default="0")):
        prole = False
        for role in ctx.guild.roles:
            if role.name.lower() == "muted":
                prole = True
                break
            else:
                prole = False
        if not prole:
            await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(permissions=2048), color=discord.Color(0x111111))
        role = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
        await user.add_roles(role, reason=reason)
        if duration == "0":
            await ctx.respond(embed=embed(ctx, title=f"Muted {user.name}", description=f"**Reason | **{reason}"))
        else:
            aum = durationConverter(duration)
            amount = aum[0]
            unit = aum[1]
            multiplier = aum[2]
            a = embed(ctx, title=f"Muted {user.name} for {amount}{unit}", description=f"**Reason | **{reason}", footer=f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | {amount}{unit}')
            b = await ctx.respond(embed=a)
            for sec in range(amount * multiplier[unit]):
                a.set_footer(text=f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | {timeConverter(amount)}')
                await b.edit_original_message(embed=a)
                await asyncio.sleep(1)
            a.set_footer(text=f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | Mute Finished')
            await b.edit_original_message(embed=a)
            await user.remove_roles(role, reason="Auto Un Mute")

    @slash_command(name="unmute", description="Un Mutes User", guild_ids=[703637471212077096])
    @default_permissions(moderate_members=True)
    async def unmute(self, ctx: discord.ApplicationContext, user: Option(discord.User, "User", required=True), reason: Option(str, "Reason", default="Un-Muted")):
        role = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
        if role in user.roles:
            await user.remove_roles(role, reason=reason)
            await ctx.respond(embed=embed(ctx, title=f"Un Muted {user.name}"))
        else:
            await ctx.respond(embed=embed(ctx, title=f"{user.name} is not muted"))

    @slash_command(name="purge", description="Deletes Messages In Bulk", guild_ids=[703637471212077096])
    @default_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: Option(int, "Amount", required=True, max_value=100)):
        await ctx.channel.purge(limit=amount)
        p = await ctx.respond(embed=embed(ctx, title=f"Successfully Purged {amount} Messages"))
        await asyncio.sleep(5)
        await p.delete_original_message()

    @slash_command(name="kick", description="Kicks People Out Of The Server")
    @default_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: Option(discord.User, "User", required=True), reason: Option(str, "Reason", default="Kicked")):
        await ctx.respond(embed=embed(ctx, title=f"Kicked {user.name}", description=f"**Reason |** {reason}"))
        await user.kick()


def setup(bot):
    bot.add_cog(Admin(bot))
