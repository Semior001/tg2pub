"""
Package pubs provides simple implementations of senders for new telegram messages.
"""
from .pubs import Publisher
from .remote import JRPC

__all__ = ['Publisher', 'JRPC']