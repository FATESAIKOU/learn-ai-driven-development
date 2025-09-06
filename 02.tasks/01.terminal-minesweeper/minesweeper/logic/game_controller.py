"""Game controller for orchestrating minesweeper game flow."""

from typing import Optional
from ..models import GameState, GameStatus, InputCommand, Difficulty, DEFAULT_DIFFICULTIES
from .game_board import GameBoard


class GameController:
    """Main game controller that orchestrates game flow and state."""
    
    def __init__(self):
        """Initialize game controller."""
        self.game_state = GameState()
        self.board: Optional[GameBoard] = None
        self.difficulties = DEFAULT_DIFFICULTIES.copy()
    
    def start_new_game(self, difficulty: Difficulty) -> None:
        """Start a new game with the specified difficulty."""
        self.board = GameBoard(difficulty)
        self.game_state.start_game(difficulty)
    
    def process_menu_command(self, command: InputCommand) -> bool:
        """
        Process command while in menu.
        
        Args:
            command: Input command to process
            
        Returns:
            True if command was handled, False to exit
        """
        if command == InputCommand.EXIT:
            self.game_state.status = GameStatus.EXITED
            return False
        
        elif command == InputCommand.MOVE_UP:
            if self.game_state.selected_menu_index > 0:
                self.game_state.selected_menu_index -= 1
        
        elif command == InputCommand.MOVE_DOWN:
            max_index = len(self.difficulties)  # +1 for exit option
            if self.game_state.selected_menu_index < max_index:
                self.game_state.selected_menu_index += 1
        
        elif command == InputCommand.SELECT:
            selected = self.game_state.selected_menu_index
            
            # Check if exit option is selected
            if selected == len(self.difficulties):
                self.game_state.status = GameStatus.EXITED
                return False
            
            # Start game with selected difficulty
            if 0 <= selected < len(self.difficulties):
                difficulty = self.difficulties[selected]
                self.start_new_game(difficulty)
                return True
        
        return True
    
    def process_game_command(self, command: InputCommand) -> bool:
        """
        Process command while in game.
        
        Args:
            command: Input command to process
            
        Returns:
            True if command was handled, False to exit to menu
        """
        if command == InputCommand.EXIT:
            # Return to menu
            self.game_state.status = GameStatus.MENU
            self.game_state.selected_menu_index = 0
            return False
        
        if self.board is None:
            return False
        
        if command == InputCommand.MOVE_UP:
            self.game_state.move_cursor(0, -1)
        
        elif command == InputCommand.MOVE_DOWN:
            self.game_state.move_cursor(0, 1)
        
        elif command == InputCommand.MOVE_LEFT:
            self.game_state.move_cursor(-1, 0)
        
        elif command == InputCommand.MOVE_RIGHT:
            self.game_state.move_cursor(1, 0)
        
        elif command == InputCommand.SELECT:
            self._handle_cell_reveal()
        
        elif command == InputCommand.FLAG:
            self._handle_cell_flag()
        
        return True
    
    def _handle_cell_reveal(self) -> None:
        """Handle cell revelation at cursor position."""
        if self.board is None or self.game_state.status != GameStatus.PLAYING:
            return
        
        x, y = self.game_state.cursor_x, self.game_state.cursor_y
        success, hit_mine = self.board.reveal_cell(x, y)
        
        if success:
            if hit_mine:
                # Game over - loss
                self.board.reveal_all_mines()
                self.game_state.status = GameStatus.LOST
            else:
                # Update revealed count
                self.game_state.cells_revealed = self.board.get_revealed_count()
                
                # Check win condition
                if self.board.is_solved():
                    self.game_state.status = GameStatus.WON
    
    def _handle_cell_flag(self) -> None:
        """Handle flag toggle at cursor position."""
        if self.board is None or self.game_state.status != GameStatus.PLAYING:
            return
        
        x, y = self.game_state.cursor_x, self.game_state.cursor_y
        cell = self.board.get_cell(x, y)
        
        if cell is None or not cell.can_flag():
            return
        
        # Get old flag state
        was_flagged = cell.is_flagged
        
        # Toggle flag
        if self.board.toggle_flag(x, y):
            # Update flag count
            if was_flagged:
                self.game_state.decrement_flags()
            else:
                self.game_state.increment_flags()
    
    def get_current_difficulty(self) -> Optional[Difficulty]:
        """Get the current game difficulty."""
        return self.game_state.current_difficulty
    
    def get_game_statistics(self) -> dict:
        """Get current game statistics."""
        return {
            'status': self.game_state.status,
            'elapsed_time': self.game_state.get_elapsed_time(),
            'remaining_mines': self.game_state.get_remaining_mines(),
            'cells_revealed': self.game_state.cells_revealed,
            'flags_placed': self.game_state.flags_placed,
        }
    
    def restart_current_game(self) -> bool:
        """Restart the current game with same difficulty."""
        if self.game_state.current_difficulty is None:
            return False
        
        self.start_new_game(self.game_state.current_difficulty)
        return True
    
    def process_game_over_command(self, command: InputCommand) -> bool:
        """
        Process command while in game over state.
        
        Args:
            command: Input command to process
            
        Returns:
            True if command was handled, False to exit
        """
        if command == InputCommand.EXIT:
            self.game_state.status = GameStatus.MENU
            self.game_state.selected_menu_index = 0
            return True
        
        elif command == InputCommand.SELECT:
            # For now, just return to menu on any selection
            # This could be expanded to handle "Play Again" options
            self.game_state.status = GameStatus.MENU
            self.game_state.selected_menu_index = 0
            return True
        
        return True
    
    def is_game_active(self) -> bool:
        """Check if game is currently being played."""
        return (
            self.game_state.status == GameStatus.PLAYING and 
            self.board is not None
        )
    
    def is_game_over(self) -> bool:
        """Check if game is in game over state."""
        return self.game_state.status in [GameStatus.WON, GameStatus.LOST]
    
    def add_custom_difficulty(self, difficulty: Difficulty) -> None:
        """Add a custom difficulty option."""
        if difficulty.is_valid():
            self.difficulties.append(difficulty)
    
    def get_menu_options(self) -> list[str]:
        """Get list of menu options for display."""
        options = [diff.name for diff in self.difficulties]
        options.append("Exit")
        return options
