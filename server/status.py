from mcstatus import JavaServer
from mcrcon import MCRcon
from collections import namedtuple
import config

serverInfo = namedtuple('serverInfo', ['players', 'num_online'])
serverInfo.__doc__ = 'Tuple containing list of online players and number of online players'
serverInfo.players.__doc__ = 'List of players currently online'
serverInfo.num_online.__doc__ = 'Integer number of players currently online'


def connect_to_server() -> JavaServer:
    """
    Connects to the server defined in config
    :return: JavaServer connection
    """
    server = JavaServer(config.SERVER, config.QUERY_PORT)
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

def _send_rcon_command(command: str) -> str:
	with MCRcon(f"{config.SERVER}", config.RCON_PASSWORD, port=config.RCON_PORT) as mcr:
		resp = mcr.command(command)
		return resp

def get_players_online() -> list[str]:
	raw_players = _send_rcon_command("/list")
	raw_players = raw_players.split(":")[1].split(",")
	players = []
	for player in raw_players:
		players.append(player.strip())

	return players
