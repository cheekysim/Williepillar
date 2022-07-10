from email.policy import default
import discord

def embed(**kwargs):
    embed=discord.Embed()
    embed.type = kwargs.get("type", embed.Empty)
    embed.title = kwargs.get("title", embed.Empty)
    embed.description = kwargs.get("description", embed.Empty)
    embed.url = kwargs.get("url", embed.Empty)
    embed.color = kwargs.get("color", embed.Empty)

    for field in kwargs.get("author", []):
        print(field)
        try:
            embed.set_author(name=field['name'], url=field['url'], icon=field['icon'])
        except:
            try:
                embed.set_author(name=field['name'])
            except:
                try:
                    embed.set_author(name=field['name'], icon=field['icon'])
                except:
                    embed.set_author(name=field['name'], url=field['url'])

    for field in kwargs.get("fields", []):
        print(field)
        try:
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        except:
            embed.add_field(name=field['name'], value=field['value'], inline=False)

    for field in kwargs.get("footer", []):
        print(field)
        try:
            embed.set_footer(text=field['text'], icon_url=field['icon'])
        except:
            embed.set_footer(text=field['text'])

    return embed