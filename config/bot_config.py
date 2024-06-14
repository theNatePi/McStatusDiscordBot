"""
All config variables for the bot as a whole
"""
import discord
from .private import load_rcon_password, load_server_address

PREFIX = '!'
"""Bot prefix to use"""

# Configure the server and port of the Minecraft server
SERVER = load_server_address()
QUERY_PORT = 5001
RCON_PORT = 7195
RCON_PASSWORD = load_rcon_password()

DELETION_COOLDOWN = 1
"""Cooldown before deleting messages queued to be deleted"""
ACTIVITY_ROTATE_COOLDOWN = 10
"""
Time in seconds that it takes for the bot's activity to rotate
One rotation also represents one tick of "cooldown" for message deletion
"""

# Allows all intents for the bot
INTENTS = discord.Intents.all()

BOT_DESCRIPTION = 'A bot which can be configured to display information ' \
                  'about users on a specific Minecraft Server'

# Names for cogs
STANDARD_COG_NAME = 'Standard Commands'
MCSTATUS_COG_NAME = 'Server Status Commands'

# Help descriptions for commands
PING_DESCRIPTION = 'Sends a ping to the bot to ensure it is working'
PING_HELP = 'Should respond with "pong"'

ONLINE_DESCRIPTION = 'Retrieves all currently online players'
ONLINE_HELP = 'Responds with a list of players'
ONLINE_ERROR = "Sorry, I couldn't get the online players :("
