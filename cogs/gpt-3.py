import json
import openai
from datetime import datetime

import discord # noqa
from discord.commands import slash_command, Option
from discord.ext import commands

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]

with open('openapi.json') as f:
    data = json.load(f)
    openapi_key = data["OPENAI_API_KEY"]


class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="gpt", description="Ask GPT-3 a question", guild_ids=guilds)
    async def gpt(self, ctx, prompt: Option(str, "What do you want to ask GPT-3?", required=True)): # noqa
        def generate_prompt(prompt):
            return f"""Q: How are you feeling?
            A: I am feeling good.
            Q: What is your name?
            A: My name is davinici.
            Q: What is human life expectancy in the United States?
            A: Human life expectancy in the United States is 78 years.
            Q: Which party did he belong to?
            A: He belonged to the Republican Party.
            Q: How does a telescope work?
            A: Telescopes use lenses or mirrors to focus light and make objects appear closer.
            Q: How much is 5 dollars in pounds?
            A: 5 dollars is 3.75 pounds.
            Q: What is 10 pounds in euros?
            A: 10 pounds is 12.5 euros
            Q: What day is it today?
            A: it is {datetime.now().strftime("%A, %B %d, %Y")}.
            Q: {prompt}
            A:"""
        openai.api_key = openapi_key
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=generate_prompt(prompt),
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=2.0
        )

        await ctx.respond(embed=embed(ctx, title="GPT-3", description=response["choices"][0]["text"]))


def setup(bot):
    bot.add_cog(GPT(bot))
