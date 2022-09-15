import json
import openai

import discord  # noqa
from discord.commands import slash_command, Option
from discord.ext import commands

import os, sys, inspect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

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
    async def gpt(self, ctx, prompt: Option(str, "What do you want to ask GPT-3?", required=True)):  # noqa
        """
        It takes a prompt, and then asks GPT-3 a bunch of questions, and then asks the prompt, and then returns the answer.
        :param ctx: The context of the command
        :param prompt: The prompt to give GPT-3
        :type prompt: Option(str, "What do you want to ask GPT-3?", required=True)
        """
        import json
        with open('gpt/main.json', 'r') as f:
            data = json.load(f)
            training = data["data"]
        try:
            with open(f'gpt/{ctx.author.id}.json', 'r') as f:
                data = json.load(f)
                user_training = data["data"][-2:]
                modified_user_training = data["data"][-2:]
                i = 0
                while len(modified_user_training) < 6:
                    modified_user_training.insert(0, training[i])
                    i += 1
                final_training = "\n".join([f"Human: {i[0]}\nAI: {i[1]}" for i in modified_user_training])
        except FileNotFoundError:
            user_training = []
            final_training = "\n".join([f"Human: {i[0]}\nAI: {i[1]}" for i in training])
        openai.api_key = openai_key
        response = openai.Completion.create(
            model="text-curie-001",
            prompt=f"AI is a chatbot that reluctantly answers questions sarcastically\n\n{final_training}\nHuman:{prompt}\nAI:",
            temperature=0.7,
            max_tokens=75,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        user_training.append([prompt, response.choices[0].text.replace('\n\n', '').lstrip()])
        data = {"data": user_training}
        with open(f"gpt/{ctx.author.id}.json", "w") as f:
            json.dump(data, f, indent=4)
        await ctx.respond(embed=embed(ctx, title="GPT-3", fields=[{'name': prompt, 'value': response.choices[0].text}]))


def setup(bot):
    bot.add_cog(GPT(bot))
