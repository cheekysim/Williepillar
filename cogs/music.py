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
import ffmpeg




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
    
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if  len(info["entries"]) == 0: return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild_id][0])
            self.song_queue[ctx.guild_id].pop(0)

    async def play_song(self, ctx,song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @slash_command(name="join", description="joins vc", guild_ids=[703637471212077096])
    async def join(self,ctx):
        if ctx.author.voice is None:
            return await ctx.respond("You must be in a voice channel for the bot to join")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        
        await ctx.author.voice.channel.connect()
    
    @slash_command(name="leave", description="leaves vc", guild_ids=[703637471212077096])
    async def leave(self,ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.respond("Not connected to a voice channel")

    @slash_command(name="play", description="plays song", guild_ids=[703637471212077096])
    async def play(self,ctx, *, song=None):
        if song is None:
            return await ctx.respond("Please include a song")
        if ctx.voice_client is None:
            return await ctx.respond("I require to be in a voice channel to play a song")
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.respond("Searching for the song, this might take a few seconds")
            result = await self.search_song(1, song, get_url=True)
            if result is None:
                return await ctx.respond("Sorry, I did not find any results.")
            song = result[0]
        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild_id])
            if queue_len < 10:
                return await ctx.respond(f"Added to queue position {queue_len+1}")
            else:
                return await ctx.respond("Can only queue up to 10 songs, please wait untill the current song is finished")
        await self.play_song(ctx, song)
        await ctx.respond(f"Now playing {song}")
    
    @slash_command(name="search", description="searches for song", guild_ids=[703637471212077096])
    async def search(self,ctx, *, song=None):
        if song is None:
            return await ctx.respond("Please enter a song to search for")
        await ctx.respond("Searching for the song, this might take a few seconds")
        info = await self.search_song(5, song)
        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song")
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount +=1
        embed.set_footer(text=f"Displaying the first {amount} results")
        await ctx.respond(embed=embed)

        @slash_command(name="queue", description="queues song", guild_ids=[703637471212077096])
        async def search(self,ctx):
            if len(self.song_queue[ctx.guild_id]) == 0:
                return await ctx.respond("There are no songs in the queue")
            
            embed = discord.Embed(title="Song Queue",descrption="",colour=discord.Colour.purple())
            i = 1
            for url in self.song_queue[ctx.guild.id]:
                embed.description += f"{i}) {url}\n"
                i += 1
            await ctx.respond(embed=embed)

        @slash_command(name="skip", description="skips song", guild_ids=[703637471212077096])
        async def skip(self,ctx):
            if ctx.voice_client is None:
                return await ctx.respond("No song is being played")
            if ctx.author.voice is None:
                return await ctx.respond("You must be in a voice channel to use this command")
            if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
                return await ctx.respond("You must be in the same voice channel as the bot to use this command")
            
            poll = discord.Embed(title=f"Vote To Skip Song", description="**80% of of the voice channel must vote to skip", colour=discord.Colour.purple())
            poll.add_feild(name="Skip", value=":white_check_mark:")
            poll.add_feild(name="Stay", value=":no_entry_sign:")
            poll.set_footer(text="Vote ends in 15 seconds")
            poll_msg = await ctx.respond(embed=poll)
            poll_id = poll_msg.id
            await poll.msg.add_reaction(u"\u2705")
            await poll.msg.add_reaction(u"\U0001F6AB")
            await asyncio.sleep(15)
            poll_msg = await ctx.channel.fetch_message(poll_id)

            votes = {u"\u2705": 0, u"\U0001F6AB": 0}
            reacted = []
            for reaction in poll_msg.reactions:
                if reaction.emoji in [u"\u2705",u"\U0001F6AB"]:
                    async for user in reaction.users():
                        if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                            votes[reaction.emoji] +=1 
                            reacted.append(user.id)
            skip = False
            if votes[u"\u2705"] > 0:
                if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79:
                    skip = True
                    embed = discord.Embed(title="Skip Successful", descrption="***Voting to skip the song was successful, skipping***", colour=discord.Colour.purple())
            
            if not skip:
                embed = discord.Embed(title="Skip Failed", descrption="***Voting to skip the song was unsuccessful***", colour=discord.Colour.purple())
            embed.set_footer(text="Voting Ended")
            await poll_msg.clear_reactions()
            await poll_msg.edit(embed=embed)
            if skip:
                ctx.voice_client.stop()



def setup(bot):
    bot.add_cog(Music(bot))

