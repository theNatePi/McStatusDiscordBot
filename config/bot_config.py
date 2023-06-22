import discord

PREFIX = '!'

INTENTS = discord.Intents.default()
INTENTS.messages = True

BOT_DESCRIPTION = 'A bot which can be configured to display information ' \
                  'about users on a specific Minecraft Server'
