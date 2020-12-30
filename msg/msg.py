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
    """
    Basic chat user, author of the message.
    """

    id: str
    username: str
    display_name: str
    is_bot: bool

    def __init__(self, id=None, username=None, display_name=None, is_bot=None):
        self.id = id
        self.username = username
        self.display_name = display_name
        self.is_bot = is_bot

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (self.id == other.id
                and self.username == other.username
                and self.display_name == other.display_name
                and self.is_bot == other.is_bot)


class Message:
    """
    Basic chat/channel message, that has to be sent to the recipients.
    """

    id: str
    chat_id: str
    chat_type: ChatType
    author: User
    sent: datetime.datetime
    text: str

    def __init__(self, id=None, chat_id=None, chat_type=None, author=None, sent=None, text=None):
        self.id = id
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.author = author
        self.sent = sent
        self.text = text

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return (self.id == other.id
                and self.chat_id == other.chat_id
                and self.chat_type == other.chat_type
                and self.author == other.author
                and self.sent == other.sent
                and self.text == other.text)


class Encoder(json.JSONEncoder):
    """Encodes the object according to its type. Timestamps will be encoded in RFC3339 format."""
    def default(self, obj):
        if isinstance(obj, Message):
            res = obj.__dict__
            res['__type__'] = 'Message'
            return res
        if isinstance(obj, User):
            res = obj.__dict__
            res['__type__'] = 'User'
            return res
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'User':
        return User(
            id=obj['id'],
            username=obj['username'],
            display_name=obj['display_name'],
            is_bot=bool(obj['is_bot'])
            )
    if '__type__' in obj and obj['__type__'] == 'Message':
        return Message(
            id=obj['id'],
            chat_id=obj['chat_id'],
            chat_type=ChatType(obj['chat_type']),
            author=obj['author'],
            sent=datetime.datetime.fromisoformat(obj['sent']),
            text=obj['text']
            )
    return obj


def decode_json(obj):
    """Public method for decoding JSON into objects from msg package."""
    return json.loads(obj, object_hook=decoder)


def encode_json(obj):
    """Public method for encoding objects from msg package."""
    return json.dumps(obj, cls=Encoder)
