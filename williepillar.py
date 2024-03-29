import json
import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(intents=intents)

# Loading the cogs and checking if they are enabled or not.
with open('config.json', 'r') as f:
    data = json.load(f)
    ids = data["ids"]
    modules = []
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            file = file[:-3]
            modules.append(file)
            try:
                if file not in data["cogs"][0]:
                    data["cogs"][0][file] = "enabled"
                if data["cogs"][0][file] in ["enabled", "broken"]:
                    bot.load_extension(f"cogs.{file}")
                    print(f"Loaded {file}")
                else:
                    print(f"Did Not Load {file}")
            except Exception as e:
                print(e)
                data["cogs"][0][file] = "broken"
                print(f"Failed to Load {file}")
        else:
            continue

    for i in list(data["cogs"][0]):
        if i in modules:
            pass
        else:
            data["cogs"][0].pop(i)

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=2)

# Loading the token from the token.json file.
with open('token.json') as f:
    data = json.load(f)
    token = data["token"]
    print("Loaded Token")


@bot.event
async def on_ready():
    print("Williepillar Online")
    await bot.change_presence(activity=discord.Game(name="With ur mum ;)"))


bot.run(token)
