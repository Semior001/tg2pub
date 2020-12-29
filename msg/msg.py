"""Module provides basic structures used by the service for publishing."""
import enum
import datetime
import json


class ChatType(enum.IntEnum):
    PRIVATE = 0
    GROUP = 1
    CHANNEL = 2
    """
    Type of the chat where the message was received from.
    """


class User:
    id: str
    username: str
    display_name: str
    is_bot: bool
    """
    Basic chat user, author of the message.
    """
    def __init__(self, id=None, username=None, display_name=None, is_bot=None):
        self.id = id
        self.username = username
        self.display_name = display_name
        self.is_bot = is_bot


class Message:
    id: str
    chat_id: str
    chat_type: ChatType
    author: User
    sent: datetime.datetime
    text: str
    """
    Basic chat/channel message, that has to be sent to the recipients.
    """
    def __init__(self, id=None, chat_id=None, chat_type=None, author=None, sent=None, text=None):
        self.id = id
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.author = author
        self.sent = sent
        self.text = text


class Encoder(json.JSONEncoder):
    """Encodes the object according to its type. Timestamps will be encoded in RFC3339 format."""
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        if isinstance(obj, User):
            return obj.__dict__
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def encode_json(obj):
    """Public method for encoding objects from msg package."""
    return json.dumps(obj, cls=Encoder)
