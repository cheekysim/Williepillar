import discord


def embed(ctx, **kwargs):
    embed = discord.Embed()
    embed.type = kwargs.get("type", embed.Empty)
    embed.title = kwargs.get("title", embed.Empty)
    embed.description = kwargs.get("description", embed.Empty)
    embed.url = kwargs.get("url", embed.Empty)
    embed.color = kwargs.get("color", 0x6600ff)
    embed.set_thumbnail(url=(kwargs.get("thumbnail", embed.Empty)))
    embed.set_image(url=(kwargs.get("image", embed.Empty)))
    embed.set_footer(text=(kwargs.get("footer", f'{ctx.bot.user.name} | Requested By: {ctx.author.name}')))

    for field in kwargs.get("author", []):
        embed.set_author(name=field.get("name", embed.Empty), url=field.get("url", embed.Empty), icon_url=field.get("icon", embed.Empty))

    for field in kwargs.get("fields", []):
        embed.add_field(name=field.get("name", embed.Empty), value=field.get("value", embed.Empty), inline=field.get("inline", False))

    return embed
