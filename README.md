# mcstatus-discordbot
A Discord bot which provides simple information on the current status of a Minecraft server

The bot can currently display the number of online players in the "status" of the bot. It can also show which users are online at any given time.

# Development
This project is a WIP, but is meant to be available for anyone to use

# Technologies used
- discord.py - Discord API python wrapper
- mcstatus - Requests API for Minecraft server status

# How To Set Up
## Dependencies
[discord.py](https://discordpy.readthedocs.io/en/stable/)

[mcstatus](https://mcstatus.io/docs) (See python-mcstatus at bottom of API page)

## Setting up the bot
1. Create and configure a Discord bot on the Discord Developer website
2. Add bot token from Discord Developer website to config/bot_token.py
3. Add bot prefix, server address, server port, and any other settings to config/bot_config.py
4. Start bot with run.py
5. Add bot to server and run !ping command to ensure the bot is online

# Commands
- !online - Show all online players by their username
- !ping - Ping the bot, should respond with "pong" if working correctly
