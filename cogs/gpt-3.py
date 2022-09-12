import json
import openai

import discord # noqa
from discord.commands import slash_command, Option
from discord.ext import commands

import os, sys, inspect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed
from modules.checks import checks

# It's loading the config.json file and setting the guilds and ids variables to the values in the
# config.json file.
with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]

# It's loading the openapi.json file and setting the openai_key variable to the value in the
# openapi.json file.
with open('openai.json') as f:
    data = json.load(f)
    openai_key = data["key"]


class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="gpt", description="Ask GPT-3 a question", guild_ids=guilds)
    async def gpt(self, ctx, prompt: Option(str, "What do you want to ask GPT-3?", required=True)): # noqa
        """
        It takes a prompt, and then asks GPT-3 a bunch of questions, and then asks the prompt, and then returns the answer.
        :param ctx: The context of the command
        :param prompt: The prompt[] to give GPT-3
        :type prompt: Option(str, "What do you want to ask GPT-3?", required=True)
        """
        with open('gpt-training.txt', 'r') as f:
            data = f.read()
            training = data

        def generate_prompt(prompt):
            return f"""
            {training}
            Q: {prompt}
            A:"""
        openai.api_key = openai_key
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=generate_prompt(prompt),
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=2.0
        )
        with open('output.txt', 'w') as f:
            f.write(response['choices'][0]['text'])
        await ctx.respond(embed=embed(ctx, title="GPT-3", fields=[{'name': prompt, 'value': response["choices"][0]["text"]}]))

    @slash_command(name="gpt_train", description="Train GPT-3", guild_ids=guilds)
    @checks.is_owner()
    async def gpt_train(self, ctx, question: Option(str, "What question do you want to train GPT-3 with?", required=True), answer: Option(str, "What answer do you want to train GPT-3 with?", required=True)): # noqa
        with open('gpt-training.txt', 'a') as f:
            f.write(f"Q: {question}\nA: {answer}\n")
        await ctx.respond(embed=embed(ctx, title="GPT-3", description="GPT-3 has been trained.", fields=[{'name': question, 'value': answer}]))


def setup(bot):
    bot.add_cog(GPT(bot))
