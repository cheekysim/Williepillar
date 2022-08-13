import json
import sys
import os
import inspect

import discord
from discord.ext import commands

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from modules.embed import embed

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]
    errors = data["errors"][0]


ignore = [commands.CommandNotFound, commands.TooManyArguments]

error_response = {
    commands.NoPrivateMessage: "This command doesn't work in private messges!",
    commands.MissingPermissions: "You are missing the **{e.missing_perms[0]}** permissions to do this!",
    commands.BotMissingPermissions: "It seams the bot doesnt have **administrator** permissions",
    commands.CommandOnCooldown: "This command is on a cooldown: Retry after {e.retry.after}. You can only use this command {e.cooldown.rate} every {e.cooldown.per} Seconds!",
    commands.BadArgument: "Oops an invalid argument has been passed!",
    commands.BadUnionArgument: "An invalid argument has been passed for {e.parent.name}!",
    commands.MissingRequiredArgument: "You need the {e.param.name} argument for this command to work!",
    commands.CheckFailure: "You do **not** have permissions to do this!",
}


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if error.__class__ in ignore:
            return
        for e in error_response:
            if isinstance(error, e):
                msg = errors[e]
                await ctx.respond(embed=embed(ctx, title=msg))
            else:
                raise error


def setup(bot):
    bot.add_cog(Errors(bot))
