from .utils import send_rcon_command
import asyncio
import datetime


async def send_eleven_eleven():
    send_rcon_command('/tellraw @a ["",{"text":"it is 11:11, ","color":"dark_purple"},{"text":"make a wish! ✨","color":"dark_purple","italic":true}]')

async def handle_server_commands(make_wish):
    # Handle the 11:11 notification
    now = datetime.datetime.now()
    if (now.hour in [11, 23]) and (now.minute == 11) and make_wish:
        await send_eleven_eleven()
        make_wish = False

    if (now.hour in [11, 23]) and (now.minute == 12):
        make_wish = True

    return make_wish

def setup_player(player_name: str):
    send_rcon_command(f'/whitelist add {player_name}')
    send_rcon_command(f'/tellraw @a "Added player {player_name}"')
