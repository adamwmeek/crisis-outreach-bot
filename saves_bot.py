import os
import logging as saves_logger
from dotenv import load_dotenv

import discord
from discord.ext import commands

KEYWORDS_FILENAME = 'keywords.txt'
RESPONSE_FILENAME = 'response.txt'
VOLUNTEER_MESSAGE = 'I picked up on a keyword in conversation: '

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
VOLUNTEER_CHANNEL_ID = int(os.getenv('VOLUNTEER_CHANNEL_ID'))

saves_logger.basicConfig(level=saves_logger.DEBUG, format='%(asctime)s %(message)s',
                    handlers=[saves_logger.FileHandler("saves_bot.log"), saves_logger.StreamHandler()])
bot = commands.Bot(command_prefix='$')
KEYWORDS = []
RESPONSE_MESSAGE = ''
client = discord.Client()

def _reload_response():
    with open(RESPONSE_FILENAME, 'r') as filehandle:
        RESPONSE_MESSAGE = ''
        contents = filehandle.readlines()

        RESPONSE_MESSAGE = ''.join(map(str, contents))
        saves_logger.debug(f'Loaded response: {RESPONSE_MESSAGE}')
        return RESPONSE_MESSAGE

RESPONSE_MESSAGE = _reload_response()

def _reload_keywords():
    KEYWORDS.clear()
    with open(KEYWORDS_FILENAME, 'r') as filehandle:
        contents = filehandle.readlines()

        for line in contents:
            line = line.strip('\r')
            line = line.strip('\n')
            KEYWORDS.append(line.lower())
            saves_logger.debug(f'Added keyword: {line}')
            
_reload_keywords()

def _add_keyword(keyword):
    KEYWORDS.append(keyword.lower())

    with open(KEYWORDS_FILENAME, 'w') as filehandle:
            filehandle.writelines(KEYWORDS)

def _remove_keyword(keyword):
    KEYWORDS.remove(keyword.lower())

    with open(KEYWORDS_FILENAME, 'w') as filehandle:
            filehandle.writelines(KEYWORDS)

@client.event
async def on_message(message):
    # Ignore messages in volunteer channel
    if message.channel.id == VOLUNTEER_CHANNEL_ID:
        return

    # Ignore messages from bots
    if message.author.bot:
        return

    # If we see a keyword in any message, take the following actions:
    if any([word in message.content for word in KEYWORDS]):
        saves_logger.debug(f'Picked up on keyword in channel {message.channel.name} in message: {message.content}')

        # Send crisis info to author of message
        await message.author.send(RESPONSE_MESSAGE)

        # Put a reply in that channel
        # await message.channel.send(RESPONSE_MESSAGE)

        # Let the volunteer channel know of the incident
        volunteer_channel = client.get_channel(VOLUNTEER_CHANNEL_ID)
        await volunteer_channel.send(VOLUNTEER_MESSAGE + message.content)

@bot.command(name='add')
async def add_keyword(context, keyword):
    # Look for commands from admins
    await context.send('test')
    if any([role.name == 'Admin' for role in context.author.roles]):
        _add_keyword(keyword)
        await context.send(f'Adding keyword: {keyword}')

@bot.command(name='remove')
async def remove_keyword(context, keyword):
    # Look for commands from admins
    await context.send('test')
    if any([role.name == 'Admin' for role in context.author.roles]):
        _remove_keyword(keyword)
        await context.send(f'Removing keyword: {keyword}')

client.run(TOKEN)