from resources.client import client
from util.config import config

if __name__ == '__main__':
    client.run(config['discord']['token'])
