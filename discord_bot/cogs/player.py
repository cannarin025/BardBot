import discord

from discord.ext import commands

from discord_bot.bot import config

from typing import Dict
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from utils.yt_scraper import YtScraper
from utils.video import Video

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.search_results: Dict[Video] = {}
        self.queue: Dict[list[Video]] = {}

    def init_params(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in self.search_results.keys():
            self.search_results[guild_id] = None
        if guild_id not in self.queue.keys():
            self.queue[guild_id] = []

    async def play_next(self, ctx, voice_client):
        guild_id = voice_client.guild.id
        video = self.queue[guild_id][0]
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        await ctx.send(f"Now playing {video.title} ({video.duration//60}:{video.duration%60})\n{video.url}")
        voice_client.play(FFmpegPCMAudio(self.queue[guild_id][0].source, **FFMPEG_OPTS), after=lambda e: self.queue[guild_id].pop(0))
        if voice_client.is_playing():
            self.search_results[guild_id] = None

    @commands.command(name = "play", help="Plays tracks based on user query. Provide url or search term.")
    async def play(self, ctx, *, query):
        self.init_params(ctx)
        guild_id = ctx.guild.id
        if not self.search_results[guild_id] and query.startswith("https://"): # user provides link
            channel = ctx.author.voice.channel
            video = YtScraper.search(query)[0]
            self.queue[guild_id].append(video)
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            if not voice_client:
                await self.bot.join_vc(channel)
                voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            if voice_client and not voice_client.is_playing():
                await self.play_next(ctx, voice_client)
            else:
                await ctx.send(f"{video.title} added to queue!")

        elif not self.search_results[guild_id]: # user does not provide link
            self.search_results[guild_id] = YtScraper.search(query, num_results=5)
            message = "Please select the video you would like to play!\n"
            for i, video in enumerate(self.search_results[guild_id]):
                message += f"**{i+1}.** {video.title} ({video.duration//60}:{video.duration%60})\n"
            await ctx.send(message)

        else: # user selects track from list of options
            channel = ctx.author.voice.channel
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            if not voice_client:
                await self.bot.join_vc(channel)
                voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            video = self.search_results[guild_id][int(ctx.kwargs["query"]) - 1]
            self.queue[guild_id].append(video)
            if voice_client and not voice_client.is_playing():
                await self.play_next(ctx, voice_client)
            else:
                await ctx.send(f"{video.title} added to queue!")

    @commands.command(name = "leave", help="Disconnects bot from channel and clears queue")
    async def leave(self, ctx):
        self.init_params(ctx)
        guild_id = ctx.guild.id
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        self.queue[guild_id] = []
        self.search_results[guild_id] = None
        if voice:
            await voice.disconnect()

    @commands.command(name = "pause", help="Pauses current song.")
    async def pause(self, ctx):
        self.init_params(ctx)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("Paused track!")
            await voice.pause()
        else:
            await ctx.send("The track is not playing!")

    @commands.command(name="resume", help="Resumes current song.")
    async def resume(self, ctx):
        self.init_params(ctx)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            await ctx.send("Resuming track...")
            await voice.resume()
        else:
            await ctx.send("The track is not paused!")

    @commands.command(name="skip", help="skips current track.")
    async def skip(self, ctx):
        self.init_params(ctx)
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.pause()
        self.queue[ctx.guild.id].pop(0)
        await self.play_next(ctx, voice)

    @commands.command(name="queue", help="Displays play queue.")
    async def queue(self, ctx):
        self.init_params(ctx)
        guild_id = ctx.guild.id
        message = "**Current queue:**\n"
        if not self.queue[guild_id]:
            message += "**the queue is empty**"
        else:
            for i, video in enumerate(self.queue[guild_id]):
                if i==0:
                    message += "**Now playing:** "
                message += f"{video.title}\n"
        await ctx.send(message)

    @commands.command(name="clearqueue", help="Clears play queue.")
    async def clear_queue(self, ctx):
        self.init_params(ctx)
        guild_id = ctx.guild.id
        self.queue[guild_id] = []

def setup(bot):
    bot.add_cog(Player(bot))
