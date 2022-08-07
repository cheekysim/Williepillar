import json
import os

from discord.commands import slash_command, Option
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

cogs = []
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        cogs.append(file[:-3])


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="reload", description="Reload a specified cog", guild_ids=[703637471212077096])
    async def reload(self, ctx, cog: Option(input_type=str, choices=cogs, required=True)):
        self.bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"Reloaded {cog}")

    @slash_command(name="list_cogs", description="List all active and deactive cogs", guild_ids=[703637471212077096])
    async def list_cogs(self, ctx):
        c = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                c.append(file[:-3])
        await ctx.respond("All Cogs:\n" + '\n'.join(c))


def setup(bot):
    bot.add_cog(Cogs(bot))
