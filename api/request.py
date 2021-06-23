import requests

from util.config import config

headers = {
    "Access-Token": config['tokens']['vime-token']
    # VimeWorld developer token. Needed to increase the number of requests per minute (300)
}


# def fetch_hash_data(query):
#     res = requests.get('https://hashes.org/api.php?key={0}&query={1}'.format(config['tokens']['hashes-api-token'], query))
#
#     return res.json()


def fetch_vime_data(login):
    res = requests.get('https://api.vimeworld.ru/user/name/{0}'.format(login), headers=headers)

    return res.json()
