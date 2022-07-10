import asyncio
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
    
    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if  len(info["entries"]) == 0: return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
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
        if not ("youtube.com/watch?" in song or "https://youru.be/" in song):
            await ctx.respond("Searching for the song, this might take a few seconds")
            result = await self.search_song(1, song, get_url=True)
            if result is None:
                return await ctx.respond("Sorry, I did not find any results.")
            song = result[0]
        if ctx.voice_client.source is not None:
            if queue_len = len(self.song_queue[ctx.guild_id])
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

def setup(bot):
    bot.add_cog(Music(bot))