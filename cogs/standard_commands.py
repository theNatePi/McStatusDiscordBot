from discord.ext import commands


class Standard(commands.Cog):
    """Standard commands which can be used to interact with the bot"""

    def __init__(self, bot):
        self._bot = bot

    # description=config.HELP_CONNECT_LONG, help=config.HELP_CONNECT_SHORT
    @commands.command(name='ping')
    async def _ping(self, ctx):
        await ctx.send('pong')
