import discord
from discord.ext import commands, tasks
from .mcstatus_commands import connect_to_server, num_players_online

class LoopedTasks(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._current_activity = 0


    @tasks.loop(seconds = 10)
    async def update_activity(self):
        activity = None
        if self._current_activity == 0:
            activity = discord.Activity(type = discord.ActivityType.listening,
                                        name = "!online / !help")
            self._current_activity = 1
        elif self._current_activity == 1:
            try:
                server = connect_to_server()
                num_players = num_players_online(server)
                activity = discord.Activity(type = discord.ActivityType.watching,
                                            name = f"{num_players} people online!")
            except Exception as exc:
                activity = discord.Activity(type = discord.ActivityType.watching,
                                            name = 'ERROR')
                print(f'ERROR in activity update, {exc}')

            self._current_activity = 0

        await self._bot.change_presence(status=discord.Status.online, activity=activity)


    def start_tasks(self):
        self.update_activity.start()
