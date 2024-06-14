"""
__init__ file for config package

config package stores all config files for the bot
"""
from .private import load_bot_token, load_bot_id
from .bot_config import *

TOKEN = load_bot_token()
BOT_ID = None
