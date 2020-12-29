#!/usr/bin/env python3
from tg import TelegramListener
import telethon
import argparse
import asyncio
import threading
import os

__description__ = 'simple telegram client service, that publishes messages' \
    + ' from any chats/channels to the desired destination'


def serve(arg):
    """
    Run the REST API server, start listening in Telegram
    """
    tgl = TelegramListener(telethon.TelegramClient('tg2pub', arg.api_id, args.api_hash),
                           None)
    loop = asyncio.get_event_loop()

    def bg_task(lp):
        asyncio.set_event_loop(lp)
        lp.run_until_complete(tgl.run())

    t = threading.Thread(target=bg_task(loop))
    t.start()


def auth(arg):
    """
    Authorize into Telegram account and create a session.
    """
    tgl = TelegramListener(telethon.TelegramClient('tg2pub', arg.api_id, arg.api_hash),
                           None)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tgl.auth())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__description__)
    # registering commands
    parser.add_argument(dest='cmd', choices=['serve', 'auth'], help='command to run')

    # registering required flags
    parser.add_argument('--api_id', dest='api_id', type=str, help='id of the telegram api',
                        default=os.environ.get('API_ID'))
    parser.add_argument('--api_hash', dest='api_hash', type=str, help='hash of the telegram api',
                        default=os.environ.get('API_HASH'))

    args = parser.parse_args()

    # checking that api id and api hash are specified
    if args.api_id is None or args.api_id == '':
        parser.print_help()
    if args.api_hash is None or args.api_hash == '':
        parser.print_help()

    # selecting a command
    if args.cmd == 'serve':
        serve(args)
    elif args.cmd == 'auth':
        auth(args)
