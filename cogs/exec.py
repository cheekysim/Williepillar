import contextlib
import io
import json
import textwrap
from traceback import format_exception

from discord.commands import slash_command, Option
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]


class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="exec", description="Allows use of the eval function", guild_ids=[703637471212077096])
    async def exec(self, ctx, *, code: Option(str, "Enter Code: ", required=True)):
        str_obj = io.StringIO()
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
                result = f"```py\n{str_obj.getvalue()}\n-- {obj}\n```"
        except Exception as e:
            result = f"```py\n{''.join(format_exception(e, e, e.__traceback__))}\n```"

        await ctx.respond(f"\n{result}\n")


def setup(bot):
    bot.add_cog(Exec(bot))
