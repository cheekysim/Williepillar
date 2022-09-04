import json
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

import discord
from discord.commands import slash_command, Option
from discord.ext import commands

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed # noqa

# It's loading the config.json file and assigning the values to the variables.
with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="quote", description="Creates a quote of the given message.", guild_ids=[703637471212077096])
    async def quote(self, ctx: discord.ApplicationContext, message: Option(str, "Message", required=True), name: Option(str, "Name", required=True)):
        """
        It takes a message and a name, and creates an image with the message and name on it.

        :param ctx: The context of the command
        :type ctx: discord.ApplicationContext
        :param message: The message to be quoted
        :type message: Option(str, "Message", required=True)
        :param name: The name of the person who said the quote
        :type name: Option(str, "Name", required=True)
        """
        W, H = (1920, 1080)
        img = Image.new('RGB', (W, H), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        min_fontsize = 72
        img_fraction = 0.7
        quoter_size = 72
        line_height = 40
        font_family = "arial.ttf"
        font = ImageFont.truetype(font_family, 1)

        def get_text_size(text, image, font):
            im = Image.new('RGB', (image.width, image.height))
            draw = ImageDraw.Draw(im)
            return draw.textsize(text, font)

        def find_font_size(text, tested_font_size, font, image, target_width_ratio):
            tested_font = ImageFont.truetype(font, tested_font_size)
            observed_width, observed_height = get_text_size(text, image, tested_font)
            estimated_font_size = tested_font_size / (observed_width / image.width) * target_width_ratio
            return round(estimated_font_size)

        def wrap_text(text, min_fontsize, tested_font_size, font, image, target_width_ratio):
            longest = 512
            line = 0
            final = text
            for i in text:
                font_size = find_font_size(i, tested_font_size, font, image, target_width_ratio)
                if font_size < longest:
                    longest = font_size
                    line = text.index(i)
            text = text[line]
            font_size = find_font_size(text, tested_font_size, font, image, target_width_ratio)
            if font_size < min_fontsize:
                txt = text.split(' ')
                middle = round(len(txt) / 2)
                part1 = " ".join([txt[i] for i in range(len(txt)) if i < middle])
                part2 = " ".join([txt[i] for i in range(len(txt)) if i >= middle])
                final.pop(line)
                final.insert(line, part1)
                final.insert(line + 1, part2)
                wrap_text(final, min_fontsize, tested_font_size, font, image, target_width_ratio)
            else:
                global final_msg
                final_msg = final
                global best_fontsize
                best_fontsize = longest

        wrap_text([message], min_fontsize, 100, font_family, img, img_fraction)
        line_count = len(final_msg)
        message = "\n".join(final_msg)
        font_size = best_fontsize
        if line_count == 1:
            h = (H / 2) - quoter_size * 0.7
            qh = h + font_size * 0.6
            anc = "mm"
            qanc = "rt"
        else:
            h = qh = (H / 2) + line_count * line_height
            anc = "md"
            qanc = "ra"
        font = ImageFont.truetype(font_family, font_size)
        draw.text((W / 2, h), f'"{message}"', fill=(255, 255, 255), font=font, anchor=anc)
        font = ImageFont.truetype(font_family, quoter_size)
        draw.text((W * img_fraction * 1.2, qh), f'- {name} {datetime.now().strftime("%d/%m/%Y")}', fill=(255, 255, 255), font=font, anchor=qanc)
        with io.BytesIO() as image_binary:
            img.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.respond(file=discord.File(fp=image_binary, filename='quote.png'))


def setup(bot):
    bot.add_cog(Quote(bot))
