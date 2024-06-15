"""
All cogs and functions relating to the use of the mcstatus library
"""
import discord
import config
from discord.ext import commands
from typing import List
from server import get_players_online, setup_player


class McStatus(commands.Cog, name = config.MCSTATUS_COG_NAME):
    """Commands which give info about the server's status"""
    def __init__(self, bot: commands.Bot):
        self._bot = bot


    @staticmethod
    def _create_online_embed(players: List[str]) -> discord.Embed:
        """
        Creates an embed for the !online command

        :param players: List of players currently online
        :return: discord.Embed to be sent by the !online command
        """
        print(players)
        if players:
            players_formatted = '\n'.join(players)
            players_formatted = f'```\n{players_formatted}\n```'

            embed = discord.Embed(title = 'The following players are online!',
                                  color = discord.Color.green(),
                                  description = players_formatted)
        else:
            embed = discord.Embed(title = 'No one is online!',
                                  color = discord.Color.red())

        return embed


    @commands.command(name = 'online', description = config.ONLINE_DESCRIPTION, help = config.ONLINE_HELP)
    async def _online(self, ctx: commands.Context):
        """
        Defines the !online command

        :param ctx: Message context sent by the Discord API
        """
        original_message = await ctx.send('Loading...')
        try:
            players = get_players_online()

            embed = self._create_online_embed(players)
            await original_message.edit(content = None, embed = embed)

            loop_cog = self._bot.get_cog('LoopedTasks')
            loop_cog.add_message_to_delete(config.DELETION_COOLDOWN, original_message)
            loop_cog.add_message_to_delete(config.DELETION_COOLDOWN, ctx.message)
        except Exception as exc:
            print(f"ERROR during !online: {exc}")
            await original_message.edit(content = config.ONLINE_ERROR)

    @commands.command(name = 'verify', description = "TODO", help = "TODO")
    async def _verify(self, ctx: commands.Context):
        """
        Defines the !online command

        :param ctx: Message context sent by the Discord API
        """
        try:
            username = ctx.message.content.split(" ")[1]
            if not username:
                raise IndexError
        except IndexError:
            await ctx.send("Please provide username with `!verify username`")
            return

        original_message = await ctx.send(f'Verifying {username}...')
        try:
            setup_player(username)

            await original_message.edit(content = f'Verified {username}!')
        except Exception as exc:
            print(f"ERROR during !verify: {exc}")
