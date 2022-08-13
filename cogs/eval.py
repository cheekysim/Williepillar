import contextlib
import io
import json
import textwrap
import sys
import os
import inspect
from traceback import format_exception

import discord
from discord.commands import slash_command, Option
from discord.ext import commands

from modules.embed import embed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="eval", description="Allows use of the eval function, Use \ for a new line.", guild_ids=[703637471212077096]) # noqa
    async def eval(self, ctx: discord.ApplicationContext, code: Option(str, "Code To Run", required=True), show_code: Option(bool, "Show Code Inputted", default=False)): # noqa
        if ctx.author.id in ids:
            str_obj = io.StringIO()
            code = code.replace(' \\', '\\').replace(' \\ ', '\\').replace('\\ ', '\\')
            code = code.split('\\')
            code = "\n".join(code)
            local_variables = {
                "commands": commands,
                "bot": self.bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message
            }

            try:
                with contextlib.redirect_stdout(str_obj):
                    exec(
                        f"async def func():\n{textwrap.indent(code, '   ')}", local_variables
                    )

                    obj = await local_variables["func"]()
                    if show_code:
                        result = f"```py\n{code}\n```\n```\n{str_obj.getvalue()}\n-- {obj}\n```"
                    else:
                        result = f"```\n{str_obj.getvalue()}\n-- {obj}\n```"

            except Exception as e:
                result = f"```py\n{''.join(format_exception(e, e, e.__traceback__))}\n```"

            await ctx.respond(f"\n{result}\n")
        else:
            await ctx.respond(embed=embed(ctx, title="Not Authorised To Use Eval Command"))


def setup(bot):
    bot.add_cog(Eval(bot))
