# <https://discordpy.readthedocs.io/en/stable/quickstart.html>

import discord
import configparser

# Parse configuration options:
config = configparser.ConfigParser()
config.read('bot.ini')
TOKEN = config['launch_options']['token']

# Initialize discord client:
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('|hello'):
        await message.channel.send('Hello!')

# Run discord client:
client.run(TOKEN)
