import telethon
from typing import List, Tuple
import msg


class TelegramClient:
    """
    Interface that describes methods that the Telegram
    client should provide in order to work with Telegram API.
    """
    def remove_event_handler(self, handler: callable):
        """
        telethon.client.updates.UpdateMethods.remove_event_handler
        """
        raise Exception("not implemented")

    def is_user_authorized(self) -> bool:
        """
        telethon.client.users.UserMethods.is_user_authorized
        """
        raise Exception("not implemented")

    def start(self):
        """
        telethon.client.auth.AuthMethods.start
        """
        raise Exception("not implemented")

    def run_until_disconnected(self):
        """
        telethon.client.updates.UpdateMethods.run_until_disconnected
        """
        raise Exception("not implemented")

    def on(self, event):
        """
        telethon.client.updates.UpdateMethods.on
        """
        raise Exception("not implemented")


class TelegramListener:
    """
    Listener for Telegram messages.
    """
    __tgcl__: TelegramClient  # telegram API client
    __sources__: List[Tuple[callable, str]] = []  # list of sources, where to take the messages

    def __init__(self, tgcl: TelegramClient, callback: callable):
        self.__tgcl__ = tgcl
        self.__callback = callback

    def add_source(self, source_name: str):
        """
        Add ID of the chat/channel to listen it for updates.
        """
        @self.__tgcl__.on(telethon.events.NewMessage(chats=[source_name]))
        async def handler(event):
            await self.__handler(event)

        self.__sources__.append((handler, source_name))

    async def __handler(self, event):
        """
        Telegram message event handler.
        """
        m = msg.Message(id=str(event.id), chat_id=str(event.chat_id),
                        sent=event.message.date, text=event.message.text)
        chat = await event.get_chat()
        if chat.is_group:
            m.chat_type = msg.ChatType.GROUP
        elif chat.is_channel:
            m.chat_type = msg.ChatType.CHANNEL
        elif chat.is_private:
            m.chat_type = msg.ChatType.PRIVATE
        else:
            # we don't want (yet) to handle the other types of chats
            return

        if event.sender is not None:
            m.author = msg.User()
            m.author.id = event.sender.sender_id
            m.author.username = event.sender.username
            m.author.display_name = telethon.utils.get_display_name(event.sender)
            m.author.is_bot = event.sender.bot

        self.__callback(m)

    def remove_source(self, source_id: str):
        """
        Stop listening the chat/channel.
        """
        # noinspection PyTypeChecker
        src_to_remove: Tuple[callable, str] = None

        for src in self.__sources__:
            if src[1] == source_id:
                src_to_remove = src

        if src_to_remove is None:
            return

        self.__tgcl__.remove_event_handler(src_to_remove[1])

    def run(self):
        """
        Run the listener.
        """
        self.__tgcl__.start()
        if not self.__tgcl__.is_user_authorized():
            raise Exception('user is not authorized')

        with self.__tgcl__ as client:
            client.run_until_disconnected()
