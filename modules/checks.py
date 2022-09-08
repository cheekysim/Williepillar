import json
from discord.ext import commands

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]


class checks():
    def __init__(self):
        self = self

    def is_owner():        async def predicate(ctx):
            if ctx.author.id in ids:
                return True
            raise commands.CheckFailure
        return commands.check(predicate)
