"""Terminal Minesweeper Game Package."""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "A terminal-based minesweeper game with keyboard navigation"

from . import models
from . import infrastructure  
from . import logic
from . import presentation

__all__ = [
    "models",
    "infrastructure", 
    "logic",
    "presentation",
]
