# <https://discordpy.readthedocs.io/en/stable/quickstart.html>

import os
import discord
from discord.ext import commands
import configparser
import logging
import yt_dlp

logging.basicConfig(level=logging.INFO)

# Parse configuration options:
config = configparser.ConfigParser()
config.read('bot.ini')
PREFIX = config['options']['prefix']
TOKEN = 'INVALID TOKEN'



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
async def cmd_play(ctx, arg1: str):
    # # voice_channel = discord.utils.get(ctx.guild.voice.channels, name='General')
    # # voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # # await voice_channel.connect()
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    # channel = ctx.message.author.voice.channel
    # server = ctx.message.guild
    # voice_channel = server.voice_client

    # async with ctx.typing():
    #     # player = await YTDLSource.from_url(url, loop=client.loop)
    #     player = await yt_dlp.YoutubeDL..from_url(url, loop=client.loop)
    #     voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    # await ctx.send('**Now playing:** {}'.format(player.title))
    voice_client = ctx.voice_client
    voice_channel = ctx.message.author.voice.channel
    await voice_channel.connect()



# Run discord client:
# client.run(TOKEN)
client.run(TOKEN)

