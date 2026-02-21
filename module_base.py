"""
This file defines the base class for all modules in the AMIF ecosystem.
It enforces a common interface and provides essential functionality for communication and status monitoring.
"""

from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ModuleBase(ABC):
    """
    Abstract Base Class (ABC) that all modules must inherit from.
    
    This class defines the core methods needed for module functionality,
    including communication, status updates, and error handling.
    """

    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        """
        Initializes a new module instance.

        Args:
            name: Unique identifier of the module.
            config: Configuration parameters for the module.
        """
        self.name = name
        self.config = config
        self.status = "INITIALIZING"
        self.broker = None  # To be set during initialization with BrokerSingleton

    def __str__(self) -> str:
        return f"Module {self.name} (Status: {self.status})"

    @abstractmethod
    def on_message(self, sender: str, message: Dict[str, Any]) -> None:
        """
        Abstract method to be implemented by subclasses.
        
        Handles incoming messages from other modules or the broker.

        Args:
            sender: Identifier of the message sender.
            message: The received message content.
        """

    def publish(self, topic: str, data: Dict[str, Any]) -> None:
        """
        Publishes a message to the broker on a specific topic.

        Args:
            topic: Topic to which the message is published.
            data: Data to be sent as part of the message.
        """
        if self.broker:
            self.broker.publish(topic=topic, message=data)
        else:
            logger.error("Broker not connected. Message not published.")

    def set_status(self, status: str) -> None:
        """
        Updates the module's operational status.

        Args:
            status: New status of the module (e.g., "OPERATIONAL", "DEGRADED").
        """
        self.status = status
        logger.info(f"Module {self.name} status updated to {status}.")
        # Optionally publish status change to a dedicated topic

    def handle_error(self, error: Exception) -> None:
        """
        Handles exceptions by logging and setting an error status.

        Args:
            error: The exception that occurred.
        """
        logger.error(f"Error in module {self.name}: {str(error)}")
        self.set_status(status="DEGRADED")

```