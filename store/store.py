import msg
from typing import List


class Store:
    """
    Store describes methods for a storage to contain and retrieve messages.
    """

    def add_source(self, source: str):
        """Add source to listen."""
        raise Exception("not implemented")

    def list_sources(self) -> List[str]:
        """Return the list of sources to listen"""
        raise Exception("not implemented")

    def remove_source(self, source: str):
        """Remove source from listening."""
        raise Exception("not implemented")

    def add_messages(self, m: List[msg.Message]):
        """Add messages to the storage."""
        raise Exception("not implemented")

    def pop_messages(self) -> List[msg.Message]:
        """Get all messages from the storage and remove them."""
        raise Exception("not implemented")
