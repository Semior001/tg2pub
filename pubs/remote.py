import msg
from .pubs import Publisher
from jsonrpcclient import request


class JRPC(Publisher):
    """
    Class JRPC implements Publisher with sending the requests to
    the remote JSON-RPC server.
    """
    __endpoint: str  # endpoint of the JSON-RPC server

    def __init__(self, endpoint):
        self.__endpoint = endpoint

    def publish_message(self, message: msg.Message):
        response = request(self.__endpoint, "publish_message", message=message)
        pass
