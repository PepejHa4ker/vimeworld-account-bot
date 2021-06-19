from datetime import datetime

import discord
from discord import Embed

from api.check import hash_found
from api.query import fetch_discord_data, fetch_data, fetch_data_collection
from api.request import fetch_vime_data, fetch_hash_data


async def set_reaction(message, reaction):
    await message.add_reaction(reaction)


async def send_profile(ctx, login):
    embed = Embed(color=discord.Colour.green())

    res = fetch_discord_data(str(login))

    embed.add_field(name="Логин", value=res['login'])
    embed.add_field(name="Баланс", value="{0}₽".format(res['balance']))

    if res['is_subscribed'] is True:
        embed.add_field(name="Подписка", value=res['subscription'], inline=False)
    else:
        embed.add_field(name="Подписан", value='False', inline=False)

    await ctx.send(embed=embed)


async def send_user(ctx, login, private: bool = True):
    user = fetch_data(str(login))

    await send_raw_user(ctx, user, private)


async def send_user_collection(ctx, email):
    res = fetch_data_collection(email)

    parsed = []

    for user in res:
        if user['login'] in parsed:
            continue

        await send_raw_user(ctx, user)

        parsed.append(user['login'])


async def send_raw_user(ctx, user, private: bool):
    embed = Embed(color=discord.Colour.green())

    embed.add_field(name="Логин", value=user['login'], inline=False)
    password = user['password']
    hash_data = fetch_hash_data(password)['result'][password]
    if not hash_found(password) or hash_data is None:
        embed.add_field(name="Пароль", value=password, inline=False)
    else:
        embed.add_field(name="Пароль", value=hash_data['plain'], inline=False)
    embed.add_field(name="Алгоритм шифрования пароля", value=user['password_version'], inline=False)
    embed.add_field(name="Дата регистрации", value=user['reg_time'], inline=False)
    embed.add_field(name="Почта", value=user['email'], inline=True)

    vime_data = fetch_vime_data(user['login'])

    if user['keys'] is not None:
        embed.add_field(name="Коды двухфакторной аутентификации", value=user['keys'], inline=False)

    emails_len = len(fetch_data_collection(user['email']))

    if emails_len > 1:
        embed.add_field(name="Аккаунтов с этой почтой", value=str(emails_len), inline=True)

    if len(vime_data) > 0:
        data = vime_data[0]

        timestamp = datetime.fromtimestamp(data['lastSeen'])

        embed.add_field(name="Последний раз был в игре", value=timestamp.strftime('%Y/%m/%d-%T'), inline=False)
        embed.add_field(name="Статус", value=data['rank'].capitalize(), inline=True)
        embed.add_field(name="Уровень", value=data['level'], inline=True)
    if private:
        await ctx.author.send(embed=embed)
    else:
        await ctx.channel.send(embed=embed)
