import discord
from discord.ext import commands, tasks
from .mcstatus_commands import connect_to_server, get_info_from_server

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
                server_info = get_info_from_server(server)
                num_players = server_info.num_online

                if num_players == 1:
                    activity_name = '1 person online!'
                elif num_players > 1:
                    activity_name = f'{num_players} people online!'
                else:
                    activity_name = '0 people online!'

                activity = discord.Activity(type = discord.ActivityType.watching,
                                            name = activity_name)
            except Exception as exc:
                activity = discord.Activity(type = discord.ActivityType.watching,
                                            name = 'ERROR')
                print(f'ERROR in activity update, {exc}')

            self._current_activity = 0

        await self._bot.change_presence(status=discord.Status.online, activity=activity)


    def start_tasks(self):
        self.update_activity.start()
