import config
from discord.ext import commands
from mcstatus import JavaServer


def connect_to_server():
    server = JavaServer(config.SERVER, config.PORT)
    return server


def players_list(server):
    status = server.status()
    players = [user['name'] for user in status.raw['players']['sample']]
    return players


def num_players_online(server):
    players = players_list(server)
    num_players = len(players)
    return num_players



class McStatus(commands.Cog, name = config.MCSTATUS_COG_NAME):
    """Commands which give info about the server's status"""

    def __init__(self, bot):
        self._bot = bot


    @commands.command(name = 'online', description = config.ONLINE_DESCRIPTION, help = config.ONLINE_HELP)
    async def _online(self, ctx):
        original_message = await ctx.send('Loading...')
        try:
            server = connect_to_server()
            players = players_list(server)
            users_connected = ', '.join(players)
            final_message = f"The following players are online!\n{users_connected}"
            await original_message.edit(content = final_message)
        except Exception as exc:
            print(f"ERROR during !online: {exc}")
            await original_message.edit(content = config.ONLINE_ERROR)
