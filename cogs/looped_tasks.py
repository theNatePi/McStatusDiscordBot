"""
All cogs which rely on looped tasks (tasks.loop)
"""
import discord
import config
from discord.ext import commands, tasks
from server import get_players_online


class LoopedTasks(commands.Cog):
    """Cog containing tasks to loop while the bot is online"""
    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self._current_activity = 0
        self._messages_to_delete = []
        self._cooldown_for_deletion = []


    def add_message_to_delete(self, cooldown: int, message: discord.Message):
        """
        Adds a message to delete later (with how much later being determined by the amount of
        cycles of the tasks loop which have passed

        :param cooldown: Integer cooldown indicating number of
                             loops before deleting the message
        :param message:  Message object to delete
        """
        self._cooldown_for_deletion.append(cooldown)
        self._messages_to_delete.append(message)


    async def _delete_messages(self):
        """
        Deletes all messages which have a cooldown of zero,
        updates cooldown on messages which do not
        """
        num_pops = 0
        for index, content in enumerate(zip(self._cooldown_for_deletion, self._messages_to_delete)):
            cooldown, message = content
            if (cooldown == 1) and (message.author.id == config.BOT_ID):
                await message.edit(content = "Deleting stale response...", embed = None)
                cooldown -= 1
                self._cooldown_for_deletion[index] = cooldown
            elif cooldown == 0:
                try:
                    await message.delete()
                except Exception as exc:
                    print(f'ERROR in activity update, {exc}')

                num_pops += 1
            else:
                cooldown -= 1
                self._cooldown_for_deletion[index] = cooldown

        for _ in range(num_pops):
            self._messages_to_delete.pop(0)
            self._cooldown_for_deletion.pop(0)


    def _get_activity_zero(self) -> discord.Activity:
        """
        Gets the desired activity when self._current_activity is 0
        :return: The activity which should be set
        """
        activity = discord.Activity(type = discord.ActivityType.listening,
                                    name = "!online / !help")
        self._current_activity = 1
        return activity


    def _get_activity_one(self) -> discord.Activity:
        """
        Gets the desired activity when self._current_activity is 1
        :return: The activity which should be set
        """
        try:
            num_players = len(get_players_online())

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

        return activity


    @tasks.loop(seconds = config.ACTIVITY_ROTATE_COOLDOWN)
    async def update_activity(self):
        """
        Updates the activity of the discord bot, rotating between the available commands
        (activity zero) and the number of players online (activity one)

        Also deletes all messages which have finished their cooldown
        """
        activity = None

        await self._delete_messages()

        if self._current_activity == 0:
            activity = self._get_activity_zero()
        elif self._current_activity == 1:
            activity = self._get_activity_one()

        await self._bot.change_presence(status=discord.Status.online, activity=activity)


    def start_tasks(self):
        """
        Represents that this cog contains tasks
        This will allow all tasks to be started AFTER the bot is run, instead of when the cog
        is added to the  bot
        """
        self.update_activity.start()
