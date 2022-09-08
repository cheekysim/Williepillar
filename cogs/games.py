import json
import random

import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from discord.ui import Button, View

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

# It's loading the config.json file and assigning the values to the variables.
with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]

flag = 0
score1 = 0
score2 = 0
turn = 1
p = None
re = 0
player1 = None
player2 = None
winState = False
bList = []


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="tictactoe", description="A game of TicTacToe", guild_ids=[703637471212077096])
    async def tictactoe(self, ctx, user: Option(discord.User, "User", required=True)):
        global turn, winState, re, p, score1, score2
        score1 = 0
        score2 = 0
        p = None
        winState = False
        turn = 1
        re = 0
        player1 = ctx.author.name
        player2 = user.name
        embed = discord.Embed(title="Player0's Turn", description=f"**{player1}: {score1}  {player2}: {score2}**",
                              colour=0x71368a)

        class TicTacToe(View):
            def __init__(self):
                super().__init__()
                rnd = random.choice([1, 2])
                global flag
                if rnd == 1:
                    flag = 0
                    embed.title = f"{player1}'s Turn [X]"
                elif rnd == 2:
                    flag = 1
                    embed.title = f"{player2}'s Turn [O]"
                b1 = Button(label="*", style=discord.ButtonStyle.gray, row=0, custom_id="0")
                b2 = Button(label="*", style=discord.ButtonStyle.gray, row=0, custom_id="1")
                b3 = Button(label="*", style=discord.ButtonStyle.gray, row=0, custom_id="2")
                b4 = Button(label="*", style=discord.ButtonStyle.gray, row=1, custom_id="3")
                b5 = Button(label="*", style=discord.ButtonStyle.gray, row=1, custom_id="4")
                b6 = Button(label="*", style=discord.ButtonStyle.gray, row=1, custom_id="5")
                b7 = Button(label="*", style=discord.ButtonStyle.gray, row=2, custom_id="6")
                b8 = Button(label="*", style=discord.ButtonStyle.gray, row=2, custom_id="7")
                b9 = Button(label="*", style=discord.ButtonStyle.gray, row=2, custom_id="8")
                bR = Button(label="Rematch 0/2", style=discord.ButtonStyle.green, row=3)

                async def rematch(interaction):
                    global p
                    global re
                    if re != 1:
                        p = interaction.user
                        re += 1
                        bR.label = f"Rematch {re}/2"
                        await interaction.response.edit_message(embed=embed, view=self)
                    elif re == 1 and interaction.user != p:
                        view = TicTacToe()
                        global turn, score1, score2
                        turn = 1
                        re = 0
                        p = None
                        embed.description = f"**{player1}: {score1}  {player2}: {score2}**"
                        await interaction.response.edit_message(embed=embed, view=view)
                    elif interaction.user == p:
                        await interaction.response.send_message("You already voted for a rematch", ephemeral=True)

                bR.callback = rematch
                bE = Button(label="Exit", style=discord.ButtonStyle.red, row=3)
                global bList
                bList = [b1, b2, b3, b4, b5, b6, b7, b8, b9, bE, bR]

                async def exit(interaction):
                    embed.title = "Exited Game."
                    await interaction.response.edit_message(view=None, embed=embed)

                bE.callback = exit
                for i in range(10):
                    self.add_item(bList[i])

                async def button_callback(interaction):
                    button = bList[int(interaction.custom_id)]
                    global turn
                    turn += 1
                    OX = ["X", "O"]
                    global winState
                    if winState is False:
                        global flag
                        if flag == 0:
                            button.label = "X"
                            flag = 1
                            button.disabled = True
                            embed.title = f"{player2}'s Turn [O]"
                            pass
                        elif flag == 1:
                            button.label = "O"
                            flag = 0
                            button.disabled = True
                            embed.title = f"{player1}'s Turn [X]"
                    if turn > 9:
                        embed.title = "It's A Tie!"
                        self.add_item(bR)
                        await interaction.response.edit_message(view=self, embed=embed)
                    for char in OX:
                        if (b1.label == char and b2.label == char and b3.label == char) or (
                                b4.label == char and b5.label == char and b6.label == char) or (
                                b7.label == char and b8.label == char and b9.label == char) or (
                                b1.label == char and b4.label == char and b7.label == char) or (
                                b2.label == char and b5.label == char and b8.label == char) or (
                                b3.label == char and b6.label == char and b9.label == char) or (
                                b1.label == char and b5.label == char and b9.label == char) or (
                                b3.label == char and b5.label == char and b7.label == char):
                            if char == "O":
                                global score2, score1
                                embed.title = f"{player2} Is The Winner!"
                                score2 += 1
                                embed.description = f"**{player1}: {score1}  {player2}: {score2}**"
                            else:
                                embed.title = f"{player1} Is The Winner!"
                                score1 += 1
                                embed.description = f"**{player1}: {score1}  {player2}: {score2}**"
                            winState = True
                            for i in range(9):
                                bList[i].disabled
                    if winState is True:
                        self.add_item(bR)
                        winState = False
                        await interaction.response.edit_message(view=self, embed=embed)
                    else:
                        await interaction.response.edit_message(view=self, embed=embed)

                for j in range(9):
                    bList[j].callback = button_callback

            async def interaction_check(self, interaction) -> bool:
                global bList

                if interaction.user != ctx.author and interaction.user != user:
                    await interaction.response.send_message("You are not a participant in this game.", ephemeral=True)
                    return False
                else:
                    if interaction.user == ctx.author and flag == 0:
                        return True
                    elif interaction.user == user and flag == 1:
                        return True
                    elif (interaction.custom_id == bList[9].custom_id or interaction.custom_id == bList[10].custom_id) and (interaction.user == ctx.author or interaction.user == user):
                        return True
                    else:
                        await interaction.response.send_message("It's not your turn.", ephemeral=True)
                        return False

        view = TicTacToe()
        await ctx.respond(embed=embed, view=view)

    @slash_command(name="8ball", description="A game of 8ball", guild_ids=[703637471212077096])
    async def ball(self, ctx, question):
        rnd = random.choice(["yes", "no", "maybe", "probably"])
        await ctx.respond(embed=embed(ctx, title=f"**A: {rnd}**", description=f"**Q: {question}**"))


def setup(bot):
    bot.add_cog(Games(bot))
