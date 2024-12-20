import logging

from ironbeam.auth.api import Auth
from ironbeam.base import Ironbeam

__all__ = [
    "Ironbeam",
    "Auth",
]

# Setup logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
