"""
This file handles module discovery using ZeroMQ's gossip protocol.
"""

import logging
from typing import List
import zmq

logger = logging.getLogger(__name__)


class DiscoveryService:
    """
    Service responsible for discovering and registering modules in the network.
    
    Uses ZeroMQ's gossip to maintain a list of active modules.
    """

    def __init__(self) -> None:
        """