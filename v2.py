import discord
from discord.ext import commands
import yt_dlp


TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : True}

@bot.command()
async def play(ctx, search):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        if not ctx.voice_client:
            vc = await voice_channel.connect()
        else:
            vc = ctx.voice_client
        
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                await ctx.send(f"Playing {title}")
                vc.play(discord.FFmpegPCMAudio(url, executable="ffmpeg", options="-vn"))
        except Exception as e:
            await ctx.send(f"Error: {e}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        vc = await voice_channel.connect()
        await ctx.send(f"Joined {voice_channel}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")@bot.command()


bot.run(TOKEN)