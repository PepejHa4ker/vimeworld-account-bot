from discord.ext import commands

from api.check import is_registered
from api.discord import send_profile
from util.config import config

from api.query import update_balance, update_subscription, fetch_discord_data


class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def qualified_name(self):
        return "Обычные"

    @commands.command()
    @commands.check(is_registered)
    async def profile(self, ctx):
        await send_profile(ctx, ctx.author)

    @commands.command()
    @commands.check(is_registered)
    async def donate(self, ctx):
        await ctx.author.send(
            """
            Для пополнения счета отправьте платеж на {0}
            \nВ комментарий к платежу прикрепите свой discord-id ({1})
            """.format(config['economy']['url'], ctx.author)
        )

    @commands.command()
    @commands.check(is_registered)
    async def subscribe_week(self, ctx):
        login = str(ctx.author)

        data = fetch_discord_data(login)

        balance = data['balance']
        cost = config['economy']['week']

        if balance < cost:
            raise ValueError()

        update_subscription(login, 7)
        update_balance(login, -cost)

    @commands.command()
    @commands.check(is_registered)
    async def subscribe_month(self, ctx):
        login = str(ctx.author)

        data = fetch_discord_data(login)

        balance = data['balance']
        cost = config['economy']['month']

        if balance < config['economy']['month']:
            raise ValueError()

        update_subscription(login, 31)
        update_balance(login, -cost)
