import os
from dotenv import load_dotenv, dotenv_values

class EnvError(Exception):
	def __init__(self, missing_item):
		super().__init__(f'Missing config/.env item "{missing_item}"')

def _load_from_env(item):
	load_dotenv()
	env_item = os.getenv(item)
	if env_item:
		return env_item

	raise EnvError(item)

def load_bot_token():
	return _load_from_env("TOKEN")

def load_rcon_password():
	return _load_from_env("RCON_PASS")

def load_server_address():
	return _load_from_env("SERVER_IP")

def load_bot_id(client):
    return client.user.id
