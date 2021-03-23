import discord
from discord.ext import commands
import logging as saves_logger

from saves_responder import SavesResponder
from user_timeout import UserTimeout

saves_logger.basicConfig(level=saves_logger.DEBUG, format='%(asctime)s %(message)s',
                        handlers=[saves_logger.FileHandler("saves_bot.log"), saves_logger.StreamHandler()])
bot = commands.Bot(command_prefix='$')
responder = SavesResponder()
user_timeout_list = UserTimeout()

""" This code decorates the on_message event and looks for keywords to react to (in the right conditons). """
@bot.event
async def on_message(message):
    # Ignore messages in volunteer channel
    if message.channel.id == responder.VOLUNTEER_CHANNEL_ID:
        return

    # Ignore messages from bots
    if message.author.bot:
        return

    # Ignore messages sent within timeout period from same user
    if user_timeout_list.check_if_user_in_timeout(message.author.name):
        return

    # Look for commands from admins
    if any([role.name == 'Admin' for role in message.author.roles]):
        await bot.process_commands(message)
        return

    # If we see a keyword in any message, take the following actions:
    if any([word in message.content.lower() for word in responder.KEYWORDS]):
        saves_logger.debug(f'Picked up on keyword in channel {message.channel.name} in message: {message.content}')

        # Send crisis info to author of message
        await message.author.send(responder.RESPONSE_MESSAGE)

        # Put a reply in that channel? (We're still discussing if we want this)
        # await message.channel.send(RESPONSE_MESSAGE)

        # Let the volunteer channel know of the incident
        volunteer_channel = bot.get_channel(responder.VOLUNTEER_CHANNEL_ID)
        await volunteer_channel.send(responder.VOLUNTEER_MESSAGE + message.content)

@bot.command(name='crisis_add')
async def add_keyword(context, keyword):
    responder._add_keyword(keyword)
    await context.send(f'Adding keyword: {keyword}')

@bot.command(name='crisis_remove')
async def remove_keyword(context, keyword):
    responder._remove_keyword(keyword)
    await context.send(f'Removing keyword: {keyword}')

bot.run(responder.TOKEN)