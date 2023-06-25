"""
The main module for mcstatus-discord bot
Should be run using "python3.11+ run.py"

mcstatus-discordbot is a Discord Bot which displays simple information
about a configured minecraft server
"""
import asyncio
import config
import cogs
from discord.ext import commands
from typing import List


COGS = [cogs.Standard, cogs.McStatus, cogs.LoopedTasks]
"""All cogs to add to the bot"""


def _start_background_tasks(cogs_to_start: List[commands.Cog]):
    """
    If a cog has background tasks, start them
    Cogs with background tasks need a "start_tasks" method

    :param cogs_to_start: Cogs to check for start_tasks method
    """
    for cog in cogs_to_start:
        if hasattr(cog, 'start_tasks'):
            cog.start_tasks()


def _define_on_ready(bot: commands.Bot, added_cogs: List[commands.Cog]):
    """
    Defines the "on_ready" event for the bot

    :param bot: commands.Bot object
    :param added_cogs: A list of cogs added to the bot
    """
    @bot.event
    async def on_ready():
        print('Ready!')
        _start_background_tasks(added_cogs)


async def _add_cogs(bot: commands.Bot) -> List[commands.Cog]:
    """
    Adds all cogs stored in COGS

    :param bot: commands.Bot object
    :return initialized_cogs: All cogs initialized (added to the bot)
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
