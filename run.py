import config
from discord.ext import commands


COGS = []
"""All cogs to add to the bot"""


def _define_on_ready(bot):
    """
    Defines the "on_ready" event for the bot
    :param bot: commands.Bot object
    """
    @bot.event
    async def on_ready():
        print('Ready!')


def _add_cogs(bot):
    """
    Adds all cogs stored in COGS
    :param bot: commands.Bot object
    """
    for cog in COGS:
        bot.add_cog(cog(mcstatus_bot))


if __name__ == "__main__":
    mcstatus_bot = commands.Bot(command_prefix = config.PREFIX,
                                description = config.BOT_DESCRIPTION,
                                intents = config.INTENTS)

    _define_on_ready(mcstatus_bot)
    _add_cogs(mcstatus_bot)
    mcstatus_bot.run(config.TOKEN)
