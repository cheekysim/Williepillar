import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import os

bot = commands.Bot(command_prefix="w/")
slash = SlashCommand(bot, sync_commands=True)

with open('Williepillar/config.json', 'r') as f:
    data = json.load(f)
    for file in os.listdir("Williepillar/cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                data["cogs"][0][file[:-3]] = "active"
                print(f"Loaded {file[:-3]}")
            except Exception as e:
                print(e)
                data["cogs"][0][file[:-3]] = "deactive"
                print(f"Failed to Load {file[:-3]}")
        else:
            continue
    with open('Williepillar/config.json', 'w') as f:
        json.dump(data, f, indent=2)

with open('Williepillar/config.json') as f:
    data = json.load(f)
    token = data["token"]
    guild_ids = data["guilds"]
    print("Loaded Token")

@bot.event
async def on_ready():
    print("Williepillar Online")
    await bot.change_presence(activity=discord.Game(name="Nothing"))

bot.run(token)