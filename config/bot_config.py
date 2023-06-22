"""
All config variables for the bot as a whole
"""
import discord

PREFIX = '!'

INTENTS = discord.Intents.default()
"""Intents used by the bot"""
INTENTS.messages = True

BOT_DESCRIPTION = 'A bot which can be configured to display information ' \
                  'about users on a specific Minecraft Server'
