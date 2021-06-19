import discord
from discord import Member
from discord.ext import commands

from api.check import user_exists, is_registered, is_subscribed
from api.discord import send_profile, send_user
from api.query import *


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def qualified_name(self):
        return "Административные"

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def force_register(self, ctx, member: Member):
        login = str(member)

        if is_subscribed(login):
            raise ValueError()

        insert_discord_data(login)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def force_unregister(self, ctx, member: Member):
        login = str(member)

        if not is_registered(login):
            raise ValueError()

        delete_discord_data(login)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get_profile(self, ctx, member: discord.Member):
        await send_profile(ctx, member)

    # MONEY MANAGEMENT
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_money(self, ctx, member: discord.Member, amount):
        login = str(member)

        if not is_registered(login):
            raise ValueError()

        update_balance(login, amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def take_money(self, ctx, member: discord.Member, amount):
        login = str(member)

        if not is_registered(login):
            raise ValueError()

        update_balance(login, '-' + amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_money(self, ctx, member: discord.Member, amount):
        login = str(member)

        if not is_registered(login):
            raise ValueError()

        set_balance(login, amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_subscription(self, ctx, member: discord.Member, days):
        login = str(member)

        if not is_registered(login):
            raise ValueError()

        update_subscription(login, days)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def demo(self, ctx, login):
        if not user_exists(login) or not await is_subscribed(str(ctx.author)):
            raise ValueError()

        await send_user(ctx, login, False)
