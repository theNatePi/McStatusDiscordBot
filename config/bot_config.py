"""
All config variables for the bot as a whole
"""
import discord

PREFIX = '!'

# INTENTS = discord.Intents.default()
"""Intents used by the bot"""
# INTENTS.messages = True
INTENTS = discord.Intents.all()

BOT_DESCRIPTION = 'A bot which can be configured to display information ' \
                  'about users on a specific Minecraft Server'

# Names for cogs
STANDARD_COG_NAME = 'Standard Commands'

# Help descriptions for commands
PING_DESCRIPTION = 'Sends a ping to the bot to ensure it is working'
PING_HELP = 'Should respond with "pong"'
