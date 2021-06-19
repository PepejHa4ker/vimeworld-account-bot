from api.query import *
from api.request import fetch_hash_data


def is_registered(ctx):
    author = str(ctx.author)

    res = fetch_discord_data(author)
    return res is not None


async def is_subscribed(login):
    data = fetch_discord_data(login)

    return data['is_subscribed']


def user_exists(login):
    return fetch_data(login) is not None


def email_exists(email):
    return len(fetch_data_collection(email)) > 0


def hash_found(password):
    return fetch_hash_data(password)['result'][password] != 'null'

