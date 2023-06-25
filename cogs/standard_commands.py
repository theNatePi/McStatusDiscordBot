"""
All cogs for standard bot commands
"""
import config
from discord.ext import commands


class Standard(commands.Cog, name = config.STANDARD_COG_NAME):
    """Standard commands which can be used to interact with the bot"""
    def __init__(self, bot):
        self._bot = bot


    @commands.command(name = 'ping', description = config.PING_DESCRIPTION, help = config.PING_HELP)
    async def _ping(self, ctx: commands.Context):
        """
        Defines the !ping command
        Simple command to ping the bot and receive a response

        :param ctx: Message context sent by the Discord API
        """
        await ctx.send('pong')
