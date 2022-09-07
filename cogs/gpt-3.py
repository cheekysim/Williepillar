import json
import openai

import discord # noqa
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

# It's loading the openapi.json file and setting the openapi_key variable to the value in the
# openapi.json file.
with open('openapi.json') as f:
    data = json.load(f)
    openapi_key = data["OPENAI_API_KEY"]


class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    It takes a prompt, and then asks GPT-3 a bunch of questions, and then asks the prompt, and then
    returns the answer.
    :param ctx: The context of the command
    :param prompt: The prompt to give GPT-3
    :type prompt: Option(str, "What do you want to ask GPT-3?", required=True)
    """

    @slash_command(name="gpt", description="Ask GPT-3 a question", guild_ids=guilds)
    async def gpt(self, ctx, prompt: Option(str, "What do you want to ask GPT-3?", required=True)): # noqa
        def generate_prompt(prompt):
            return f"""
            A is a chatbot that reluctantly answers questions with sarcastic responses:

            Q: How many pounds are in a kilogram?
            A: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
            Q: What does HTML stand for?
            A: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
            Q: When did the first airplane fly?
            A: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
            Q: What is the meaning of life?
            A: I’m not sure. I’ll ask my friend Google.
            Q: How were you created?
            A: I was created by a bunch of nerds who wanted to make a chatbot.
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
