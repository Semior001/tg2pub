#!/usr/bin/env python3
from tg import TelegramListener
import telethon
import argparse

__description__ = 'simple telegram client service, that publishes messages' \
    + ' from any chats/channels to the desired destination'


def main(arg):
    """
    Entry point of the service
    """
    tgl = TelegramListener(telethon.TelegramClient('tg2pub', arg.api_id, args.api_hash),
                           None)
    tgl.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('--api_id', dest='api_id', type=str, help='id of the telegram api',
                        required=True)
    parser.add_argument('--api_hash', dest='api_hash', type=str, help='hash of the telegram api',
                        required=True)
    args = parser.parse_args()

    main(args)
