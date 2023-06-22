import asyncio
import config
import cogs
from discord.ext import commands


COGS = [cogs.Standard, cogs.McStatus, cogs.LoopedTasks]
"""All cogs to add to the bot"""


def _start_background_tasks(cogs_to_start):
    for cog in cogs_to_start:
        if hasattr(cog, 'start_tasks'):
            cog.start_tasks()


def _define_on_ready(bot, added_cogs):
    """
    Defines the "on_ready" event for the bot
    :param bot: commands.Bot object
    """
    @bot.event
    async def on_ready():
        print('Ready!')
        _start_background_tasks(added_cogs)


async def _add_cogs(bot):
    """
    Adds all cogs stored in COGS
    :param bot: commands.Bot object
    """
    initialized_cogs = []
    for cog in COGS:
        initialized_cog = cog(bot)
        initialized_cogs.append(initialized_cog)
        await bot.add_cog(initialized_cog)
    return initialized_cogs


if __name__ == "__main__":
    mcstatus_bot = commands.Bot(command_prefix = config.PREFIX,
                                description = config.BOT_DESCRIPTION,
                                intents = config.INTENTS)

    cogs = asyncio.run(_add_cogs(mcstatus_bot))
    _define_on_ready(mcstatus_bot, cogs)
    mcstatus_bot.run(config.TOKEN)
