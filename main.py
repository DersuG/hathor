# <https://discordpy.readthedocs.io/en/stable/quickstart.html>

import os
import discord
from discord.ext import commands
import configparser
import logging

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
bot = commands.Bot(command_prefix=PREFIX)

@bot.command(name='about')
async def cmd_about(ctx, *args):
    if len(args) == 0:
        await ctx.send('About (doesn\'t exist yet)')
    elif len(args) == 1:
        if args[0] == 'about':
            await ctx.send('about [command] - Shows help info.')
        elif args[0] == 'say':
            await ctx.send('say <message> - Make me say something.')

@bot.command(name='say')
async def cmd_say(ctx, arg1):
    await ctx.send(arg1)

@bot.command(name='ping')
async def cmd_ping(ctx):
    await ctx.send('pong')



# Run discord client:
# client.run(TOKEN)
bot.run(TOKEN)

