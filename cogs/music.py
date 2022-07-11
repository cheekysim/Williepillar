import asyncio
from asyncio.proactor_events import _ProactorDuplexPipeTransport
from asyncore import poll
from pydoc import describe
from sre_constants import SUCCESS
from tabnanny import check
from charset_normalizer import set_logging_handler
import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import asyncio
import json
import youtube_dl
import pafy





with open('config.json') as f:
    data = json.load(f)
    guild_ids = data["guilds"]

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.setup()
    
    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @slash_command(name="join", description="joins vc", guild_ids=[703637471212077096])
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.respond("You are not connected to a voice channel, please connect to the channel you want the bot to join.")
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        await ctx.author.voice.channel.connect()
    
    @slash_command(name="leave", description="leaves vc", guild_ids=[703637471212077096])
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        await ctx.respond("I am not connected to a voice channel.")

    @slash_command(name="play", description="plays song", guild_ids=[703637471212077096])
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.respond("You must include a song to play.")
        if ctx.voice_client is None:
            return await ctx.respond("I must be in a voice channel to play a song.")
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.respond("Searching for song, this may take a few seconds.")
            result = await self.search_song(1, song, get_url=True)
            if result is None:
                return await ctx.respond("Sorry, I could not find the given song, try using my search command.")
            song = result[0]
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])
            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.respond(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")
            else:
                return await ctx.respond("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")
        await self.play_song(ctx, song)
        await ctx.respond(f"Now playing: {song}")
    

    @slash_command(name="search", description="searches for song", guild_ids=[703637471212077096])
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.respond("You forgot to include a song to search for.")
        await ctx.respond("Searching for song, this may take a few seconds.")
        info = await self.search_song(5, song)
        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.dark_purple())
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1
        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.respond(embed=embed)

    @slash_command(name="queue", description="queues song", guild_ids=[703637471212077096])
    async def queue(self, ctx): 
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.respond("There are currently no songs in the queue.")
        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"
            i += 1
        embed.set_footer(text="Thanks for using me!")
        await ctx.respond(embed=embed)


    @slash_command(name="skip", description="skips song", guild_ids=[703637471212077096])
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.respond("I am not playing any song.")
        if ctx.author.voice is None:
            return await ctx.respond("You are not connected to any voice channel.")
        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.respond("I am not currently playing any songs for you.")
        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")
        poll_msg = await ctx.respond(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id
        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        await asyncio.sleep(15) # 15 seconds to vote
        poll_msg = await ctx.channel.fetch_message(poll_id)
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []
        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)
        skip = False
        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())
        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.dark_purple())
        embed.set_footer(text="Voting has ended.")
        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)
        if skip:
            ctx.voice_client.stop()

    @slash_command(name="pause", description="pause song", guild_ids=[703637471212077096])
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.respond("I am already paused.")
        ctx.voice_client.pause()
        await ctx.respond("The current song has been paused.")

    @slash_command(name="resume", description="resume song", guild_ids=[703637471212077096])
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.respond("I am not connected to a voice channel.")
        if not ctx.voice_client.is_paused():
            return await ctx.respond("I am already playing a song.")
    
        ctx.voice_client.resume()
        await ctx.respond("The current song has been resumed.")


def setup(bot):
    bot.add_cog(Music(bot))






