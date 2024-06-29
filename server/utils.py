from mcrcon import MCRcon
from io import BytesIO
from PIL import Image
import requests
import config

def send_rcon_command(command: str) -> str:
	with MCRcon(f"{config.SERVER}", config.RCON_PASSWORD, port=config.RCON_PORT) as mcr:
		resp = mcr.command(command)
		return resp

def _make_api_request(url: str) -> requests.Response:
	response = requests.get(url)
	response.raise_for_status()  # Raise an error on bad status code
	return response

def _get_image_from_response(response: requests.Response) -> Image.Image:
	image = Image.open(BytesIO(response.content))
	return image

def get_player_head(url: str) -> Image.Image:
	response = _make_api_request(url)
	head = _get_image_from_response(response)
	return head