"""
REST-based node that interfaces with MADSci and provides a USB camera interface
"""

import traceback
from pathlib import Path
from typing import Annotated, Any, Optional, Union

from madsci.common.ownership import get_current_ownership_info
from madsci.common.types.node_types import RestNodeConfig
from madsci.node_module.helpers import action
from madsci.node_module.rest_node_module import RestNode
from pydantic import field_validator
import time



class PersonNodeConfig(RestNodeConfig):
    """Configuration for the person node module."""


class PersonNode(RestNode):
    """Node that interfaces with MADSci and provides a USB camera interface"""

    config: PersonNodeConfig = PersonNodeConfig()
    config_model = PersonNodeConfig
    state_error_latch: bool = False
    waiting: bool = False

    @action
    def await_input(self) -> None:
        """
        A non-blocking action that can be used to keep the node alive and responsive while waiting for input. This can be useful in scenarios where the node needs to maintain a connection or perform background tasks without blocking the main thread.
        """
        self.logger.info("Function received...")
        if self.waiting:
            return  # Already waiting, do nothing
        self.logger.info("Node is now waiting for input.")
        self.waiting = True
        while self.waiting:
            time.sleep(0.1)  # Sleep briefly to prevent busy-waiting

    @action(blocking=False)
    def release_wait(self) -> None:
        """
        A non-blocking action that can be used to stop waiting for input. This can be useful in scenarios where the node needs to maintain a connection or perform background tasks without blocking the main thread.
        """
        self.waiting = False


if __name__ == "__main__":
    person_node = PersonNode()
    person_node.start_node()
