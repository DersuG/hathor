# <https://discordpy.readthedocs.io/en/stable/quickstart.html>

import os
import discord
from discord.ext import commands
import configparser
import logging
import yt_dlp
import asyncio

logging.basicConfig(level=logging.INFO)

# Parse configuration options:
config = configparser.ConfigParser()
config.read('bot.ini')
PREFIX = config['options']['prefix']
TOKEN = 'INVALID TOKEN'


ytdlp_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'outtmpl': 'temp/%(title)s.%(ext)s'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdlp = yt_dlp.YoutubeDL(ytdlp_format_options)

class YTLDPSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ''
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdlp.extract_info(url, download=not stream))
        if 'entries' in data:
            # Take the first item from a playlist:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdlp.prepare_filename(data)
        # filename = 'temp/' + filename
        return filename


# Attempt to read secret token:
if os.path.exists('token.txt'):
    file = open('token.txt','r') # Open file in read mode.
    lines = file.readlines()
    if len(lines) >= 1:
        TOKEN = lines[0]
else:
    file = open('token.txt', 'w+') # Open or create file in write mode.
    file.write('put your bot\'s secret token here')
    logging.log(logging.ERROR, 'token.txt not found, so it was created. Please put your bot\'s secret token inside.')
    quit(-1)



# Commands documentation <https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html>
client = commands.Bot(command_prefix=PREFIX)

@client.command(name='about')
async def cmd_about(ctx, *args):
    if len(args) == 0:
        await ctx.send('About (doesn\'t exist yet)')
    elif len(args) == 1:
        if args[0] == 'about':
            await ctx.send('about [command] - Shows help info.')
        elif args[0] == 'say':
            await ctx.send('say <message> - Make me say something.')

@client.command(name='say')
async def cmd_say(ctx, arg1: str):
    await ctx.send(arg1)

@client.command(name='ping')
async def cmd_ping(ctx):
    await ctx.send('pong')

# Via <https://www.youtube.com/watch?v=ml-5tXRmmFk>
# And <https://github.com/RK-Coding/Videos/blob/master/rkcodingmusic.py>
@client.command(name='play')
async def cmd_play(ctx, url: str):
    if not ctx.message.author.voice:
        await ctx.send("You\'re not in a voice channel")
        return

    voice_client = ctx.voice_client
    voice_channel = ctx.message.author.voice.channel
    try:
        await voice_channel.connect()
    except discord.ClientException: # Already connected or something.
        pass
    
    try:
        server = ctx.message.guild
        voice_client = server.voice_client

        async with ctx.typing():
            filename = await YTLDPSource.from_url(url, loop=False, stream=False)
            voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        # await ctx.send(f'**Now playing:** {filename}')
    except:
        await ctx.send('I\'m not in a voice channel')

@client.command(name='stop')
async def cmd_stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send('I\'m not in a voice channel')

@client.command(name='playsong')
async def cmd_playsong(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTLDPSource.from_url(url, loop=False, stream=True)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send(f'**Now playing:** {filename}')
    except:
        await ctx.send('I\'m not in a voice channel')


# Run discord client:
# client.run(TOKEN)
client.run(TOKEN)

