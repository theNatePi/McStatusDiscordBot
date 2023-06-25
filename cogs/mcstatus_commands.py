"""
All cogs and functions relating to the use of the mcstatus library
"""
import discord
import config
from discord.ext import commands
from collections import namedtuple
from mcstatus import JavaServer
from typing import List


serverInfo = namedtuple('serverInfo', ['players', 'num_online'])
serverInfo.__doc__ = 'Tuple containing list of online players and number of online players'
serverInfo.players.__doc__ = 'List of players currently online'
serverInfo.num_online.__doc__ = 'Integer number of players currently online'


def connect_to_server() -> JavaServer:
    """
    Connects to the server defined in config
    :return: JavaServer connection
    """
    server = JavaServer(config.SERVER, config.PORT)
    return server


def get_info_from_server(server: JavaServer) -> serverInfo:
    """
    Gets info from JavaServer connection

    :param server: JavaServer connection from connect_to_server method
    :return: ServerInfo namedtuple
    """
    status = server.status().raw
    num_online = status['players']['online']
    if num_online == 0:
        server_info = serverInfo([], num_online)
    else:
        players = [user['name'] for user in status['players']['sample']]
        server_info = serverInfo(players, num_online)

    return server_info



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
            server = connect_to_server()
            server_info = get_info_from_server(server)
            players = server_info.players

            embed = self._create_online_embed(players)
            await original_message.edit(content = None, embed = embed)

            loop_cog = self._bot.get_cog('LoopedTasks')
            loop_cog.add_message_to_delete(config.DELETION_COOLDOWN, original_message)
            loop_cog.add_message_to_delete(config.DELETION_COOLDOWN, ctx.message)
        except Exception as exc:
            print(f"ERROR during !online: {exc}")
            await original_message.edit(content = config.ONLINE_ERROR)
