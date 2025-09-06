"""
Data models and enums for Terminal Minesweeper game.

This module contains the core data structures used throughout the application.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


@dataclass
class Cell:
    """Represents a single cell on the minesweeper board."""
    has_mine: bool = False
    is_revealed: bool = False
    is_flagged: bool = False
    adjacent_mines: int = 0
    
    def can_reveal(self) -> bool:
        """Check if cell can be revealed."""
        return not self.is_revealed and not self.is_flagged
    
    def can_flag(self) -> bool:
        """Check if cell can be flagged."""
        return not self.is_revealed
    
    def get_display_char(self, is_game_over: bool = False) -> str:
        """Get the character to display for this cell."""
        if self.is_flagged and not is_game_over:
            return 'F'
        elif self.is_flagged and is_game_over and not self.has_mine:
            return 'X'  # Wrong flag
        elif self.has_mine and (is_game_over or self.is_revealed):
            return '*'
        elif not self.is_revealed:
            return '█'  # Hidden cell
        elif self.adjacent_mines == 0:
            return ' '  # Empty revealed cell
        else:
            return str(self.adjacent_mines)  # Number of adjacent mines


@dataclass
class Difficulty:
    """Game difficulty configuration."""
    name: str
    width: int
    height: int
    mine_count: int
    
    def is_valid(self) -> bool:
        """Validate difficulty parameters."""
        return (self.width > 0 and self.height > 0 and 
                0 < self.mine_count < self.width * self.height)
    
    def get_description(self) -> str:
        """Get formatted description of difficulty."""
        return f"{self.name} ({self.width}x{self.height}, {self.mine_count} mines)"


class GameStatus(Enum):
    """Current game state."""
    MENU = "menu"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
    EXITED = "exited"


class InputCommand(Enum):
    """User input commands."""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    SELECT = "select"
    FLAG = "flag"
    EXIT = "exit"
    INVALID = "invalid"


class Colors:
    """ANSI color codes for terminal display."""
    # Text colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_WHITE = '\033[47m'
    
    # Special effects
    INVERSE = '\033[7m'
    
    # Number colors for minesweeper
    NUMBER_COLORS = {
        1: BLUE,
        2: GREEN,
        3: RED,
        4: MAGENTA,
        5: '\033[91m',  # Bright red
        6: CYAN,
        7: BLACK,
        8: BRIGHT_BLACK
    }


# Predefined difficulty levels
DIFFICULTIES = {
    'Beginner': Difficulty('Beginner', 9, 9, 10),
    'Intermediate': Difficulty('Intermediate', 16, 16, 40),
    'Expert': Difficulty('Expert', 30, 16, 99)
}


def create_custom_difficulty(width: int, height: int, mine_count: int) -> Difficulty:
    """Create a custom difficulty configuration."""
    difficulty = Difficulty('Custom', width, height, mine_count)
    if not difficulty.is_valid():
        raise ValueError(f"Invalid difficulty parameters: {width}x{height} with {mine_count} mines")
    return difficulty


# Type aliases for better code readability
Position = Tuple[int, int]
BoardSize = Tuple[int, int]
