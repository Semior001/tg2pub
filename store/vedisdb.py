from typing import List

import msg
from .store import Store
import vedis

SRC_BKT_NAME = 'src'
MSG_BKT_NAME = 'msg'


class VedisDB(Store):
    """
    Implements Store with the VedisDB.

    The store has the next buckets:
    - msg - the list of unpublished messages
    - src - the list of sources to listen
    """

    _db: vedis.Vedis

    def __init__(self, location: str):
        self._db = vedis.Vedis(location)
        self._db.Set(SRC_BKT_NAME)
        self._db.List(MSG_BKT_NAME)

    def add_source(self, source: str):
        s = self._db.Set(SRC_BKT_NAME)
        s.add(source)

    def list_sources(self) -> List[str]:
        s = self._db.Set(SRC_BKT_NAME)
        return [source.decode("utf-8") for source in s]

    def remove_source(self, source: str):
        s = self._db.Set(SRC_BKT_NAME)
        del s[source]

    def add_messages(self, msgs: List[msg.Message]):
        bkt: List = self._db.List(MSG_BKT_NAME)
        bkt.extend([msg.encode_json(m) for m in msgs])

    def pop_messages(self) -> List[msg.Message]:
        bkt: List = self._db.List(MSG_BKT_NAME)
        res = []
        while len(bkt) > 0:
            res.append(msg.decode_json(bkt.pop().decode("utf-8")))
        return res
