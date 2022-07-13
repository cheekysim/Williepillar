from pydoc import describe
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
from discord.ui import Button, View
import random


with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]

embed = discord.Embed(title="Player0's Turn",colour=0x71368a)
flag = 0
player1 = None
player2 = None

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="tictactoe", description="A game of TicTacToe", guild_ids=[703637471212077096])
    async def tictactoe(self, ctx, user: Option(discord.User, "User", required=True)):
        player = ctx.author
        class TicTacToe(View):
            def __init__(self): 
                super().__init__()
                rnd = random.choice([1,2])
                if rnd == 1:
                    player1 = user
                    player2 = player
                    embed.title = f"{player1}'s Turn"
                elif rnd == 2:
                    player1 = player
                    player2 = user
                    embed.title = f"{player1}'s Turn"
                button1 = Button(label="*", style=discord.ButtonStyle.gray, row = 0, custom_id="0")
                button2 = Button(label="*", style=discord.ButtonStyle.gray, row = 0, custom_id="1")
                button3 = Button(label="*", style=discord.ButtonStyle.gray, row = 0, custom_id="2")
                button4 = Button(label="*", style=discord.ButtonStyle.gray, row = 1, custom_id="3")
                button5 = Button(label="*", style=discord.ButtonStyle.gray, row = 1, custom_id="4")
                button6 = Button(label="*", style=discord.ButtonStyle.gray, row = 1, custom_id="5")
                button7 = Button(label="*", style=discord.ButtonStyle.gray, row = 2, custom_id="6")
                button8 = Button(label="*", style=discord.ButtonStyle.gray, row = 2, custom_id="7")
                button9 = Button(label="*", style=discord.ButtonStyle.gray, row = 2, custom_id="8")
                bList = [button1,button2,button3,button4,button5,button6,button7,button8,button9]
                for i in range(9):
                    self.add_item(bList[i])
                async def button_callback(interaction):
                    button = bList[int(interaction.custom_id)]
                    global flag
                    if flag == 1:
                        button.label = "X"
                        flag = 2
                        button.disabled = True
                        embed.title = f"{player1}'s Turn"
                    elif flag == 1:
                        button.label = "O"
                        flag = 0
                        button.disabled = True
                        embed.title = f"{player2}'s Turn"
                    await interaction.response.edit_message(view=self, embed=embed)
                for j in range(9):
                    bList[j].callback = button_callback
                async def interaction_check(self, interaction) -> bool:
                    if interaction.user != self.ctx.author and interaction.user != user:
                        await interaction.response.send_message("You are not a participant in this game.")
                        return False
                    else:
                        return True
        view = TicTacToe()
        await ctx.respond(embed = embed,view = view)
    
    @slash_command(name="8ball",description="A game of 8ball", guild_ids=[703637471212077096])
    async def ball(self, ctx, question):
        rnd = random.choice(["yes","no","maybe","probably"])
        await ctx.respond(embed=embed(self, ctx, title=f"**A: {rnd}**",description=f"**Q: {question}**"))

def setup(bot):
    bot.add_cog(Games(bot))

