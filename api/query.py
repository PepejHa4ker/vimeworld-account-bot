from datetime import datetime
from dateutil.relativedelta import relativedelta
from util import database


def fetch_discord_data(login):
    res = database.fetch_single(
        """
        SELECT * FROM public.discord
        WHERE login = %s
        """, (login,), optional=True
    )

    return res


def fetch_data(login):
    res = database.fetch_single(
        """
        SELECT * FROM public.users
        LEFT JOIN oauth o on users.id = o.id
        WHERE login = %s
        """, (login,), optional=True
    )

    return res


def fetch_data_collection(email):
    res = database.fetch_collection(
        """
        SELECT * FROM public.users
        LEFT JOIN oauth o on users.id = o.id
        WHERE email = %s LIMIT 10
        """, (email,)
    )

    return res


def insert_discord_data(login):
    database.run_sql(
        """
        INSERT INTO public.discord (login)
        VALUES (%s) 
        """, (login,)
    )


def delete_discord_data(login):
    database.run_sql(
        """
        DELETE FROM public.discord
        WHERE login=%s
        """, (login,)
    )


def update_subscription(login, days):
    days = int(days)
    login = str(login)

    if days == 0:
        database.run_sql(
            """
            UPDATE public.discord
            SET is_subscribed = False, subscription = %s
            WHERE login = %s
            """, (None, login)
        )

        return

    timestamp = datetime.now() + relativedelta(days=days)

    database.run_sql(
        """
        UPDATE public.discord
        SET is_subscribed = True, subscription = %s
        WHERE login = %s
        """, (timestamp.strftime('%Y/%m/%d %T.%f'), login)
    )


def update_balance(login, balance):
    database.run_sql(
        """
        UPDATE public.discord 
        SET balance = balance + %s
        WHERE login = %s
        """, (balance, login)
    )


def set_balance(login, balance):
    database.run_sql(
        """
        UPDATE public.discord 
        SET balance = %s
        WHERE login = %s
        """, (balance, login)
    )
