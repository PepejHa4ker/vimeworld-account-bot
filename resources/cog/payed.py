from discord.ext import commands

from api.check import *
from api.discord import send_user, send_user_collection


class Payed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def qualified_name(self):
        return "Платные"

    @commands.command()
    @commands.guild_only()
    @commands.check(is_registered)
    async def user(self, ctx, login):
        if not user_exists(login) or not await is_subscribed(str(ctx.author)):
            raise ValueError()

        await send_user(ctx, login)

    @commands.command()
    @commands.guild_only()
    @commands.check(is_registered)
    async def email(self, ctx, email):
        if not email_exists(email) or not await is_subscribed(str(ctx.author)):
            raise ValueError()

        await send_user_collection(ctx, email)

    # @commands.command()
    # @commands.guild_only()
    # @commands.check(is_registered)
    # async def hash(self, ctx, encrypted):
    #     if not await is_subscribed(str(ctx.author)):
    #         raise ValueError()
    #     hash_data = fetch_hash_data(encrypted)['result'][encrypted]
    #     if hash_data is None:
    #         raise ValueError()
    #     embed = Embed(color=discord.Colour.red())
    #     embed.add_field(name="Хеш", value=encrypted, inline=False)
    #     embed.add_field(name="Пароль", value=hash_data['plain'], inline=False)
    #     embed.add_field(name="Алгоритм", value=hash_data['algorithm'], inline=False)
    #     await ctx.author.send(embed=embed)
