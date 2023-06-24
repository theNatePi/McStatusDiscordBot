import discord
import config
from discord.ext import commands
from collections import namedtuple
from mcstatus import JavaServer


serverInfo = namedtuple('serverInfo', ['players', 'num_online'])


def connect_to_server():
    server = JavaServer(config.SERVER, config.PORT)
    return server


def get_info_from_server(server):
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

    def __init__(self, bot):
        self._bot = bot


    @staticmethod
    def _create_online_embed(players):
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
    async def _online(self, ctx):
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
