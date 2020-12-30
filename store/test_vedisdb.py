from unittest import TestCase

from .vedisdb import VedisDB, SRC_BKT_NAME, MSG_BKT_NAME
import msg
import datetime
import operator


class TestVedisDB(TestCase):
    def test_add_source(self):
        svc = VedisDB(':mem:')  # store in memory
        svc.add_source('test_source')
        src_list = svc._db.Set(SRC_BKT_NAME)
        self.assertIn('test_source', src_list)

    def test_remove_source(self):
        svc = VedisDB(':mem:')  # store in memory
        src_list = svc._db.Set(SRC_BKT_NAME)
        src_list.add('test_source')
        svc.remove_source('test_source')
        self.assertNotIn('test_source', src_list)

    def test_list_sources(self):
        svc = VedisDB(':mem:')  # store in memory
        src_list = svc._db.Set(SRC_BKT_NAME)
        src_list.add('1', '2', '3', '4', '5')
        res = svc.list_sources()
        res.sort()
        self.assertListEqual(res, ['1', '2', '3', '4', '5'])

    def test_add_messages(self):
        svc = VedisDB(':mem:')  # store in memory
        msg_list = svc._db.List(MSG_BKT_NAME)
        expected = [
            msg.Message(id="1", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test"),
            msg.Message(id="2", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test1"),
            msg.Message(id="3", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test2")
            ]

        svc.add_messages(expected)

        expected.sort(key=operator.attrgetter('text'))

        actual = [msg.decode_json(m.decode("utf-8")) for m in msg_list]
        actual.sort(key=operator.attrgetter('text'))

        self.assertListEqual(expected, actual)

    def test_pop_messages(self):
        svc = VedisDB(':mem:')  # store in memory
        msg_list = svc._db.List(MSG_BKT_NAME)
        expected = [
            msg.Message(id="1", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test"),
            msg.Message(id="2", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test1"),
            msg.Message(id="3", chat_id="123",
                        chat_type=msg.ChatType.GROUP,
                        author=msg.User(id="123", username="semior",
                                        display_name="yelsh", is_bot=False),
                        sent=datetime.datetime(2011, 11, 4, 0, 0), text="test2")
            ]

        msg_list.extend([msg.encode_json(m) for m in expected])

        actual = svc.pop_messages()
        actual.sort(key=operator.attrgetter('text'))

        self.assertListEqual(expected, actual)
        self.assertEqual(0, len(msg_list))
