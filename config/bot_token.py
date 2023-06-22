"""
This module redirects the token of the bot
The token is kept in config/real_token.py which is included in .gitignore
This is done to prevent the token from becoming public
"""
from .real_token import REAL_TOKEN

TOKEN = REAL_TOKEN
