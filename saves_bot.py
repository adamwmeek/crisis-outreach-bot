import discord
from discord.ext import commands
import logging as saves_logger

from saves_responder import SavesResponder

saves_logger.basicConfig(level=saves_logger.DEBUG, format='%(asctime)s %(message)s',
                    handlers=[saves_logger.FileHandler("saves_bot.log"), saves_logger.StreamHandler()])
bot = commands.Bot(command_prefix='$')
client = discord.Client()
responder = SavesResponder()

""" This code decorates the on_message event and looks for keywords to react to (in the right conditons). """
@client.event
async def on_message(message):
    # Ignore messages in volunteer channel
    if message.channel.id == responder.VOLUNTEER_CHANNEL_ID:
        return

    # Ignore messages from bots
    if message.author.bot:
        return

    # If we see a keyword in any message, take the following actions:
    if any([word in message.content.lower() for word in responder.KEYWORDS]):
        saves_logger.debug(f'Picked up on keyword in channel {message.channel.name} in message: {message.content}')

        # Send crisis info to author of message
        await message.author.send(responder.RESPONSE_MESSAGE)

        # Put a reply in that channel? (We're still discussing if we want this)
        # await message.channel.send(RESPONSE_MESSAGE)

        # Let the volunteer channel know of the incident
        volunteer_channel = client.get_channel(responder.VOLUNTEER_CHANNEL_ID)
        await volunteer_channel.send(responder.VOLUNTEER_MESSAGE + message.content)

@bot.command(name='add')
async def add_keyword(context, keyword):
    # Look for commands from admins
    await context.send('test')
    if any([role.name == 'Admin' for role in context.author.roles]):
        responder._add_keyword(keyword)
        await context.send(f'Adding keyword: {keyword}')

@bot.command(name='remove')
async def remove_keyword(context, keyword):
    # Look for commands from admins
    await context.send('test')
    if any([role.name == 'Admin' for role in context.author.roles]):
        responder._remove_keyword(keyword)
        await context.send(f'Removing keyword: {keyword}')

client.run(responder.TOKEN)