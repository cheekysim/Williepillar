import json
import math
from PIL import Image, ImageDraw
import io

import discord
from discord.commands import slash_command, Option
from discord.ext import commands

from modules.embed import embed

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]
    ids = data["ids"]


class Graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="graph", description="Creates a graph of the given equation. For example, x ** 2", guild_ids=[703637471212077096])
    async def graph(self, ctx: discord.ApplicationContext, expression: Option(str, "Expression. For example, x ** 2", required=True), steps: Option(int, "Steps", default=4), substeps: Option(int, "SubSteps", default=2), show_points: Option(bool, "Show Points", default=False)): # noqa
        W, H = 1080, 1080
        grid_fill = (128, 128, 128)
        points = []

        img = Image.new('RGB', (W, H), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        def upscale(x=1, y=1, W=1, H=1, max_x=1, max_y=1):
            x = x * (W / max_x)
            y = y * (H / max_y)
            if x != 1 and y != 1:
                return x, y
            elif x == 1:
                return x
            elif y == 1:
                return y

        def grid(W, H, steps):
            for i in range(0, steps + 1):
                y = i * (H / steps)
                y -= steps / H
                if i == steps / 2:
                    draw.line([(0, y), (W, y)], fill=grid_fill, width=3)
                else:
                    draw.line([(0, y), (W, y)], fill=grid_fill, width=1)
            for i in range(0, steps + 1):
                x = i * (W / steps)
                x -= steps / W
                if i == steps / 2:
                    draw.line([(x, 0), (x, H)], fill=grid_fill, width=3)
                else:
                    draw.line([(x, 0), (x, H)], fill=grid_fill, width=1)

        grid(W, H, steps * 2)

        def even_width(x1, y1, x2, y2, width):
            x1 -= width / 8
            y1 -= width / 8
            x2 -= width / 8
            y2 -= width / 8
            return x1, y1, x2, y2

        def draw_point(x, y, width=5, fill=(255, 0, 0)):
            x1, y1, x2, y2 = even_width(x - width, y - width, x + width, y + width, width)
            draw.ellipse([(x1 + W / 2, y1 + H / 2), (x2 + W / 2, y2 + H / 2)], fill=fill)

        def f(expression, x, y):
            return eval(expression, {"math": math}, {"x": x, "y": y})

        substeps += 1
        y = 0
        for x in range((steps * - 1) * (substeps + 1), (steps + 1) * substeps):
            x /= substeps
            y = f(expression, x, y)
            points.append((x, y))

        Steps = [x for x in range(steps * - 1, steps + 1)]

        max_x = max_y = len(Steps) - 1

        for point in range(0, len(points) - 1):
            p1x, p1y = upscale(points[point][0], points[point][1], W, H, max_x, max_y)
            p2x, p2y = upscale(points[point + 1][0], points[point + 1][1], W, H, max_x, max_y)
            x1, y1, x2, y2 = even_width(p1x + (W / 2), p1y * -1 + (H / 2), p2x + (W / 2), p2y * -1 + (H / 2), 5)
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255), width=5)

        if show_points:
            for point in range(0, len(points)):
                x, y = upscale(points[point][0], points[point][1], W, H, max_x, max_y)
                draw_point(x, y * -1, 2)

        with io.BytesIO() as image_binary:
            img.save(image_binary, "PNG")
            image_binary.seek(0)
            await ctx.respond(file=discord.File(fp=image_binary, filename='graph.png'))


def setup(bot):
    bot.add_cog(Graph(bot))
