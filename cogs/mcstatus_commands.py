"""
All cogs and functions relating to the use of the mcstatus library
"""
import discord
import config
from discord.ext import commands
from typing import List
from server import get_players_online, setup_player
from PIL import Image
from io import BytesIO
import os

class McStatus(commands.Cog, name = config.MCSTATUS_COG_NAME):
    """Commands which give info about the server's status"""
    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @staticmethod
    def _create_embed_player_image(previous_images, next_image):
        image1 = previous_images.convert("RGBA")
        image2 = next_image.convert("RGBA")
        gap = 10

        (width1, height1) = image1.size
        (width2, height2) = image2.size

        result_width = width1 + gap + width2
        result_height = max(height1, height2)

        # Create a new image with RGBA mode to support transparency
        result = Image.new('RGBA', (result_width, result_height), (255, 255, 255, 0))
        result.paste(im = image1, box = (0, 0))

        # Extract the alpha channel of the second image
        image2_alpha = image2.split()[-1]
        result.paste(im = image2, box = (width1 + gap, 0), mask = image2_alpha)

        # Save the merged image as PNG to preserve transparency
        return result

    def _create_online_embed(self, players: List[tuple[str, Image.Image]]) -> discord.Embed:
        """
        Creates an embed for the !online command

        :param players: List of players currently online
        :return: discord.Embed to be sent by the !online command
        """
        file = None

        if players:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "temp.png")

            usernames = []
            for player in players:
                usernames.append(player[0])

            image = players[0][1]
            if len(players) > 1:
                for player in players[1:]:
                    image = self._create_embed_player_image(image, player[1])


            image.save(file_path)

            players_formatted = '\n'.join(usernames)
            players_formatted = f'```\n{players_formatted}\n```'

            embed = discord.Embed(title = 'The following players are online!',
                                  color = discord.Color.green(),
                                  description = players_formatted)
            embed.set_footer(text = "This message will disappear when outdated")

            file = discord.File(file_path, filename = "image.png")
            embed.set_image(url = "attachment://image.png")

            os.remove(file_path)
        else:
            embed = discord.Embed(title = 'No one is online!',
                                  color = discord.Color.red())

        return embed, file

    @commands.command(name = 'online', description = config.ONLINE_DESCRIPTION, help = config.ONLINE_HELP)
    async def _online(self, ctx: commands.Context):
        """
        Defines the !online command

        :param ctx: Message context sent by the Discord API
        """
        loading_message = await ctx.send('Loading...')
        try:
            _loop_cog = self._bot.get_cog('LoopedTasks')
            players = _loop_cog.online_player_cache

            embed, file = self._create_online_embed(players)
            # await original_message.edit(content = None, embed = embed)
            await loading_message.delete()
            original_message = await ctx.send(content = None, embed = embed, file = file)


            _loop_cog.add_message_to_previous(original_message)
            _loop_cog.add_message_to_previous(ctx.message)
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
