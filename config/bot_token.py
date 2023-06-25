"""
This module redirects the token of the bot
The token is kept in config/hidden.py which is included in .gitignore
This is done to prevent the token from becoming public
"""
from .hidden import REAL_TOKEN

TOKEN = REAL_TOKEN
