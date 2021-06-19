#!/usr/bin/python3

import sys
from argparse import ArgumentParser

from peewee_migrate import Router

from util.database import db

router = Router(db)

parser = ArgumentParser(description='Peewee migration wrapper')

parser.add_argument('action', metavar='action', type=str,
                    help='migrate / create / rollback')

parser.add_argument('name', default=None, metavar='migration name', type=str)

args = parser.parse_args()

if args.action == 'create':
    if args.name:
        try:
            router.create(args.name)
        except Exception as e:
            print(e)
            print('Can`t create migration "{0}". Exiting'.format(args.name))
            sys.exit(1)
    else:
        ArgumentParser.error()

elif args.action == 'migrate':
    if args.name == 'all':
        try:
            router.run()
        except Exception as e:
            print(e)
            print('Can`t apply migrations. Exiting')
            sys.exit(1)
    else:
        try:
            router.run(args.name)
        except Exception as e:
            print(e)
            print('Can`t apply migration "{0}". Exiting'.format(args.name))
            sys.exit(1)

elif args.action == 'rollback':

    try:
        router.rollback(args.name)
    except Exception as e:
        print(e)
        print('Can`t apply migration "{0}". Exiting'.format(args.name))
        sys.exit(1)

else:
    ArgumentParser.error()
