import peewee_async

from util.config import config

db = peewee_async.PostgresqlDatabase(
    config['database'].pop('database'),
    **config['database'],
    autorollback=True
)


def run_sql(sql, args=None):
    if args is None:
        args = []

    return db.execute_sql(sql, args)


def fetch_collection(sql, args=None):
    if args is None:
        args = []

    cursor = db.execute_sql(sql, args)

    col_names = [col[0] for col in cursor.description]
    res = [dotdict(dict(zip(col_names, row))) for row in cursor.fetchall()]

    return res


def fetch_single(sql, args, optional=False):
    cursor = db.execute_sql(sql, args)

    col_names = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row is None:
        if not optional:
            raise ValueError('Failed to fetch')
        return None

    res = dotdict(dict(zip(col_names, row)))

    return res


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
