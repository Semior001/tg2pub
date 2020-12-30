from unittest import TestCase
import json
import datetime
from msg import Message, ChatType, User, encode_json
from io import StringIO


class Test(TestCase):
    def test_jsonify(self):
        msg = Message(id="1", chat_id="123", chat_type=ChatType.GROUP,
                      author=User(id="123", username="semior", display_name="yelsh", is_bot=False),
                      sent=datetime.datetime(2011, 11, 4, 0, 0), text="test")
        s = encode_json(msg)
        # noinspection PyTypeChecker
        unloaded = json.load(StringIO(s))
        expected_as_dict = {'__type__': 'Message', 'id': '1', 'chat_id': '123', 'chat_type': 1,
                            'author': {
                                '__type__': 'User',
                                'id': '123',
                                'username': 'semior',
                                'display_name': 'yelsh',
                                'is_bot': False
                            },
                            'sent': '2011-11-04T00:00:00', 'text': 'test'}
        self.assertEqual(unloaded, expected_as_dict)
