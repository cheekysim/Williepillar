import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

with open('config.json', 'r') as f:
    data = json.load(f)
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                data["cogs"][0][file[:-3]] = "working"
                print(f"Loaded {file[:-3]}")
            except Exception as e:
                print(e)
                data["cogs"][0][file[:-3]] = "broken"
                print(f"Failed to Load {file[:-3]}")
        else:
            continue
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=2)

with open('token.json') as f:
    data = json.load(f)
    token = data["token"]
    print("Loaded Token")

@bot.event
async def on_ready():
    print("Williepillar Online")
    await bot.change_presence(activity=discord.Game(name="Nothing"))


bot.run(token)