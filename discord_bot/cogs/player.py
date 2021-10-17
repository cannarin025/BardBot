import discord
from discord.ext import commands

from discord_bot.bot import config

from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from utils.yt_scraper import YtScraper

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice_client: discord.VoiceClient = None

    @commands.command(name = "play")
    async def play(self, ctx, *, query):
        # Solves a problem I'll explain later
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        video, source = YtScraper.search(query)

        await self.bot.join_vc(ctx, self.voice_client)
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        await ctx.send(f"Now playing {video['title']}.")

        voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        voice.is_playing()

def setup(bot):
    bot.add_cog(Player(bot))
