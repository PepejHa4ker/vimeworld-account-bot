import discord

from api.discord import set_reaction
from api.query import insert_discord_data
from discord.embeds import Embed

from util.config import config
from util.logger import logger


async def on_command_error(ctx, error):
    await set_reaction(ctx.message, '\U0000274c')

    logger.error("Command error occurred ({0})".format(error))


async def on_command_completion(ctx):
    await set_reaction(ctx.message, '\U00002714')
    logger.success("Command successfully completed ({0})".format(ctx.message.content))


async def on_ready():
    logger.info("Ready.")


async def on_member_join(member):
    login = str(member)
    logger.info("{0} joined.".format(login))
    embed = Embed(color=discord.Colour.blue(), description=config['discord']['join_message'].format(str(member)))
    await member.send(embed=embed)

    insert_discord_data(login)
