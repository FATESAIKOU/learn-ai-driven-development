"""Game board logic for minesweeper."""

from typing import List, Set, Tuple, Optional
from ..models import Cell, Difficulty
from .mine_generator import MineGenerator


class GameBoard:
    """Manages the minesweeper game board state and operations."""
    
    def __init__(self, difficulty: Difficulty):
        """Initialize game board with given difficulty."""
        self.difficulty = difficulty
        self.width = difficulty.width
        self.height = difficulty.height
        self.mine_count = difficulty.mine_count
        
        # Initialize empty board
        self.cells: List[List[Cell]] = [
            [Cell() for _ in range(self.width)] 
            for _ in range(self.height)
        ]
        
        self.mine_positions: Set[Tuple[int, int]] = set()
        self.is_initialized = False
        self.mine_generator = MineGenerator()
    
    def initialize_mines(self, safe_position: Tuple[int, int]) -> None:
        """
        Initialize mine placement after first click.
        
        Args:
            safe_position: Position that must be safe (first click)
        """
        if self.is_initialized:
            return
        
        # Generate mine positions
        self.mine_positions = self.mine_generator.generate_mines(
            self.difficulty, safe_position
        )
        
        # Place mines on board
        for x, y in self.mine_positions:
            self.cells[y][x].has_mine = True
        
        # Calculate adjacent mine counts
        self._calculate_adjacent_counts()
        
        self.is_initialized = True
    
    def _calculate_adjacent_counts(self) -> None:
        """Calculate adjacent mine counts for all cells."""
        for y in range(self.height):
            for x in range(self.width):
                if not self.cells[y][x].has_mine:
                    count = self._count_adjacent_mines(x, y)
                    self.cells[y][x].adjacent_mines = count
    
    def _count_adjacent_mines(self, x: int, y: int) -> int:
        """Count mines adjacent to a specific position."""
        count = 0
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                adj_x, adj_y = x + dx, y + dy
                
                if (self._is_valid_position(adj_x, adj_y) and 
                    self.cells[adj_y][adj_x].has_mine):
                    count += 1
        
        return count
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def reveal_cell(self, x: int, y: int) -> Tuple[bool, bool]:
        """
        Reveal a cell and potentially adjacent cells.
        
        Args:
            x, y: Position to reveal
            
        Returns:
            Tuple of (success, hit_mine)
            success: True if cell was revealed
            hit_mine: True if revealed cell was a mine
        """
        if not self._is_valid_position(x, y):
            return False, False
        
        cell = self.cells[y][x]
        
        if not cell.can_reveal():
            return False, False
        
        # Initialize mines on first reveal
        if not self.is_initialized:
            self.initialize_mines((x, y))
            cell = self.cells[y][x]  # Refresh cell reference
        
        # Reveal the cell
        cell.reveal()
        
        # Check if it's a mine
        if cell.has_mine:
            return True, True
        
        # Auto-reveal adjacent cells if this cell has no adjacent mines
        if cell.adjacent_mines == 0:
            self._auto_reveal_adjacent(x, y)
        
        return True, False
    
    def _auto_reveal_adjacent(self, x: int, y: int) -> None:
        """Automatically reveal adjacent cells for zero-mine cells."""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                adj_x, adj_y = x + dx, y + dy
                
                if (self._is_valid_position(adj_x, adj_y) and 
                    self.cells[adj_y][adj_x].can_reveal()):
                    
                    # Recursively reveal adjacent cells
                    self.reveal_cell(adj_x, adj_y)
    
    def toggle_flag(self, x: int, y: int) -> bool:
        """
        Toggle flag state of a cell.
        
        Args:
            x, y: Position to flag/unflag
            
        Returns:
            True if flag state was changed
        """
        if not self._is_valid_position(x, y):
            return False
        
        cell = self.cells[y][x]
        return cell.toggle_flag()
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at position, or None if invalid position."""
        if not self._is_valid_position(x, y):
            return None
        return self.cells[y][x]
    
    def get_revealed_count(self) -> int:
        """Get number of revealed cells."""
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.is_revealed:
                    count += 1
        return count
    
    def get_flag_count(self) -> int:
        """Get number of flagged cells."""
        count = 0
        for row in self.cells:
            for cell in row:
                if cell.is_flagged:
                    count += 1
        return count
    
    def is_solved(self) -> bool:
        """Check if board is solved (all non-mine cells revealed)."""
        if not self.is_initialized:
            return False
        
        for row in self.cells:
            for cell in row:
                if not cell.has_mine and not cell.is_revealed:
                    return False
        return True
    
    def reveal_all_mines(self) -> None:
        """Reveal all mines (called when game is lost)."""
        for x, y in self.mine_positions:
            self.cells[y][x].is_revealed = True
    
    def get_adjacent_positions(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get list of valid adjacent positions."""
        positions = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                adj_x, adj_y = x + dx, y + dy
                
                if self._is_valid_position(adj_x, adj_y):
                    positions.append((adj_x, adj_y))
        
        return positions
    
    def get_board_state_string(self) -> str:
        """Get a string representation of the board for debugging."""
        lines = []
        
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                cell = self.cells[y][x]
                
                if cell.is_flagged:
                    line += "F"
                elif not cell.is_revealed:
                    line += "█"
                elif cell.has_mine:
                    line += "*"
                elif cell.adjacent_mines > 0:
                    line += str(cell.adjacent_mines)
                else:
                    line += " "
            
            lines.append(line)
        
        return "\n".join(lines)
