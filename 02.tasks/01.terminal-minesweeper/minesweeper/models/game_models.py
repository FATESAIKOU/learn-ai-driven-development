"""Core data models for Terminal Minesweeper game."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import time


class GameStatus(Enum):
    """Current game state."""
    MENU = "menu"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
    EXITED = "exited"


class InputCommand(Enum):
    """Available input commands."""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    SELECT = "select"
    FLAG = "flag"
    EXIT = "exit"
    UNKNOWN = "unknown"


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
    
    def reveal(self) -> bool:
        """Reveal the cell. Returns True if successful."""
        if self.can_reveal():
            self.is_revealed = True
            return True
        return False
    
    def toggle_flag(self) -> bool:
        """Toggle flag state. Returns True if successful."""
        if self.can_flag():
            self.is_flagged = not self.is_flagged
            return True
        return False


@dataclass
class Difficulty:
    """Game difficulty configuration."""
    name: str
    width: int
    height: int
    mine_count: int
    
    def __post_init__(self):
        """Validate difficulty parameters."""
        if not self.is_valid():
            raise ValueError(f"Invalid difficulty configuration: {self}")
    
    def is_valid(self) -> bool:
        """Validate difficulty parameters."""
        return (
            self.width > 0 and 
            self.height > 0 and 
            0 < self.mine_count < self.width * self.height
        )
    
    def total_cells(self) -> int:
        """Get total number of cells."""
        return self.width * self.height
    
    def safe_cells(self) -> int:
        """Get number of safe (non-mine) cells."""
        return self.total_cells() - self.mine_count


@dataclass
class GameState:
    """Current game state and statistics."""
    status: GameStatus = GameStatus.MENU
    cursor_x: int = 0
    cursor_y: int = 0
    start_time: Optional[float] = None
    flags_placed: int = 0
    cells_revealed: int = 0
    current_difficulty: Optional[Difficulty] = None
    selected_menu_index: int = 0
    
    def start_game(self, difficulty: Difficulty) -> None:
        """Initialize game state for new game."""
        self.status = GameStatus.PLAYING
        self.start_time = time.time()
        self.cursor_x = 0
        self.cursor_y = 0
        self.flags_placed = 0
        self.cells_revealed = 0
        self.current_difficulty = difficulty
    
    def get_elapsed_time(self) -> int:
        """Get elapsed game time in seconds."""
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)
    
    def get_remaining_mines(self) -> int:
        """Get remaining mine count (total - flags placed)."""
        if self.current_difficulty is None:
            return 0
        return self.current_difficulty.mine_count - self.flags_placed
    
    def is_cursor_valid(self) -> bool:
        """Check if cursor position is within board bounds."""
        if self.current_difficulty is None:
            return False
        return (
            0 <= self.cursor_x < self.current_difficulty.width and
            0 <= self.cursor_y < self.current_difficulty.height
        )
    
    def move_cursor(self, dx: int, dy: int) -> bool:
        """Move cursor by delta. Returns True if successful."""
        if self.current_difficulty is None:
            return False
        
        new_x = max(0, min(self.cursor_x + dx, self.current_difficulty.width - 1))
        new_y = max(0, min(self.cursor_y + dy, self.current_difficulty.height - 1))
        
        if new_x != self.cursor_x or new_y != self.cursor_y:
            self.cursor_x = new_x
            self.cursor_y = new_y
            return True
        return False
    
    def increment_flags(self) -> None:
        """Increment flag count."""
        self.flags_placed += 1
    
    def decrement_flags(self) -> None:
        """Decrement flag count."""
        if self.flags_placed > 0:
            self.flags_placed -= 1
    
    def increment_revealed(self) -> None:
        """Increment revealed cell count."""
        self.cells_revealed += 1
    
    def check_win_condition(self) -> bool:
        """Check if player has won the game."""
        if self.current_difficulty is None:
            return False
        return self.cells_revealed == self.current_difficulty.safe_cells()


# Predefined difficulty levels
DEFAULT_DIFFICULTIES = [
    Difficulty("Beginner", 9, 9, 10),
    Difficulty("Intermediate", 16, 16, 40),
    Difficulty("Expert", 30, 16, 99),
]
