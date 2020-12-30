import msg
from .pubs import Publisher
import jsonrpcserver as jrpc
import store
from typing import List
import tg


class JRPC(Publisher):
    """
    Class JRPC implements Publisher with JSON-RPC server
    """
    __store: store.Store  # store contains unpublished messages and sources

    def __init__(self, s: store.Store, tgl: tg.TelegramListener):
        self.__store = s
        self.__tgl = tgl

        self.__methods = jrpc.methods.Methods()
        self.__register_methods()

    def __register_methods(self):
        @jrpc.method(name='get_updates')
        def get_updates():
            return self.__get_updates()

        @jrpc.method(name='add_source')
        def add_source(src: str):
            self.__add_source(src)

    def __get_updates(self) -> List[msg.Message]:
        msgs = self.__store.pop_messages()
        return [msg.encode_json(m) for m in msgs]

    def __add_source(self, src: str):
        self.__store.add_source(src)
        self.__tgl.add_source(src)

    # noinspection PyMethodMayBeStatic
    def start(self, port: int):
        jrpc.serve('0.0.0.0', port)

