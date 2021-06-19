import discord
from discord.ext.commands import Bot

from resources.cog.admin import Admin
from resources.cog.common import Common
from resources.cog.payed import Payed
from resources.help import HelpCommand
from resources.listener import on_ready, on_command_completion, on_member_join, on_command_error

intents = discord.Intents.default()
intents.members = True

client = Bot(command_prefix='!', intents=intents)
client.add_cog([cog for cog in [Common(client), Payed(client), Admin(client)]])
client.add_listener(on_command_error)
client.add_listener(on_ready)
client.add_listener(on_command_completion)
client.add_listener(on_member_join)

client.help_command = HelpCommand()

