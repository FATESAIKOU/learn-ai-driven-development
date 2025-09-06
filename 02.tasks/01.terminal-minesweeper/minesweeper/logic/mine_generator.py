"""Mine generation logic for minesweeper game."""

import random
from typing import Set, Tuple
from ..models import Difficulty


class MineGenerator:
    """Generates random mine placement for minesweeper boards."""
    
    def __init__(self, seed: int = None):
        """Initialize mine generator with optional seed for testing."""
        self.random = random.Random(seed)
    
    def generate_mines(
        self, 
        difficulty: Difficulty, 
        safe_position: Tuple[int, int] = None
    ) -> Set[Tuple[int, int]]:
        """
        Generate mine positions for a board.
        
        Args:
            difficulty: Game difficulty configuration
            safe_position: Position that must not contain a mine (first click)
            
        Returns:
            Set of (x, y) positions containing mines
        """
        if not difficulty.is_valid():
            raise ValueError(f"Invalid difficulty: {difficulty}")
        
        # Get all possible positions
        all_positions = {
            (x, y) 
            for x in range(difficulty.width) 
            for y in range(difficulty.height)
        }
        
        # Remove safe position if specified
        if safe_position is not None:
            x, y = safe_position
            if 0 <= x < difficulty.width and 0 <= y < difficulty.height:
                all_positions.discard((x, y))
                
                # Also remove adjacent positions for easier first click
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        adj_x, adj_y = x + dx, y + dy
                        if (0 <= adj_x < difficulty.width and 
                            0 <= adj_y < difficulty.height):
                            all_positions.discard((adj_x, adj_y))
        
        # Ensure we have enough positions for mines
        available_positions = len(all_positions)
        if difficulty.mine_count > available_positions:
            raise ValueError(
                f"Cannot place {difficulty.mine_count} mines in "
                f"{available_positions} available positions"
            )
        
        # Randomly select mine positions
        mine_positions = set(
            self.random.sample(
                list(all_positions), 
                min(difficulty.mine_count, available_positions)
            )
        )
        
        return mine_positions
    
    def is_mine_placement_valid(
        self, 
        mine_positions: Set[Tuple[int, int]], 
        difficulty: Difficulty
    ) -> bool:
        """
        Validate that mine placement is correct.
        
        Args:
            mine_positions: Set of mine positions
            difficulty: Game difficulty
            
        Returns:
            True if placement is valid
        """
        # Check mine count
        if len(mine_positions) != difficulty.mine_count:
            return False
        
        # Check all positions are within bounds
        for x, y in mine_positions:
            if not (0 <= x < difficulty.width and 0 <= y < difficulty.height):
                return False
        
        return True
    
    def calculate_adjacent_mines(
        self, 
        mine_positions: Set[Tuple[int, int]], 
        difficulty: Difficulty
    ) -> dict[Tuple[int, int], int]:
        """
        Calculate adjacent mine counts for all board positions.
        
        Args:
            mine_positions: Set of mine positions
            difficulty: Game difficulty
            
        Returns:
            Dictionary mapping (x, y) -> adjacent mine count
        """
        adjacent_counts = {}
        
        for x in range(difficulty.width):
            for y in range(difficulty.height):
                if (x, y) not in mine_positions:
                    count = self._count_adjacent_mines(x, y, mine_positions, difficulty)
                    adjacent_counts[(x, y)] = count
        
        return adjacent_counts
    
    def _count_adjacent_mines(
        self, 
        x: int, 
        y: int, 
        mine_positions: Set[Tuple[int, int]], 
        difficulty: Difficulty
    ) -> int:
        """Count mines adjacent to a specific position."""
        count = 0
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the center position
                
                adj_x, adj_y = x + dx, y + dy
                
                # Check bounds
                if (0 <= adj_x < difficulty.width and 
                    0 <= adj_y < difficulty.height and
                    (adj_x, adj_y) in mine_positions):
                    count += 1
        
        return count
    
    def generate_solvable_board(
        self, 
        difficulty: Difficulty, 
        safe_position: Tuple[int, int] = None,
        max_attempts: int = 100
    ) -> Set[Tuple[int, int]]:
        """
        Generate a solvable mine layout.
        
        This is a basic implementation that ensures the first click area is safe.
        More sophisticated solvability checking could be added later.
        
        Args:
            difficulty: Game difficulty
            safe_position: Safe starting position
            max_attempts: Maximum generation attempts
            
        Returns:
            Set of mine positions
        """
        for attempt in range(max_attempts):
            try:
                mines = self.generate_mines(difficulty, safe_position)
                
                # Basic solvability check: ensure there are some number-only regions
                adjacent_counts = self.calculate_adjacent_mines(mines, difficulty)
                
                # Count positions with low adjacent mine counts (easier to solve)
                low_count_positions = sum(
                    1 for count in adjacent_counts.values() 
                    if count <= 2
                )
                
                # Ensure at least 30% of safe positions have low mine counts
                safe_positions = difficulty.safe_cells()
                if low_count_positions >= safe_positions * 0.3:
                    return mines
                    
            except ValueError:
                continue
        
        # Fallback: return any valid mine placement
        return self.generate_mines(difficulty, safe_position)
