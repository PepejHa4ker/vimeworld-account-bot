from api.query import *


def is_registered(ctx):
    author = str(ctx.author)

    res = fetch_discord_data(author)
    return res is not None


async def is_subscribed(login):
    data = fetch_discord_data(login)
    return data['is_subscribed']


def user_exists(login):
    return user_data_by_login(login) is not None


def email_exists(email):
    return len(users_data_by_email(email)) > 0
