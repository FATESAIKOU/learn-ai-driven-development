"""Game board rendering for minesweeper."""

from typing import Optional
from ..infrastructure import TerminalManager
from ..models import GameState, Cell
from ..logic import GameBoard


class GameRenderer:
    """Renders the game board and status information."""
    
    def __init__(self, terminal: TerminalManager):
        """Initialize game renderer."""
        self.terminal = terminal
        
        # Display characters
        self.chars = {
            'hidden': '█',
            'cursor_hidden': '▓',
            'revealed_empty': ' ',
            'flag': 'F',
            'mine': '*',
            'wrong_flag': 'X',
        }
        
        # Border characters
        self.borders = {
            'horizontal': '═',
            'vertical': '║', 
            'top_left': '╔',
            'top_right': '╗',
            'bottom_left': '╚',
            'bottom_right': '╝',
            'cross': '╬',
            't_down': '╦',
            't_up': '╩',
            't_right': '╠',
            't_left': '╣',
        }
    
    def render_game(self, board: GameBoard, game_state: GameState) -> None:
        """Render the complete game screen."""
        self.terminal.clear_screen()
        
        # Get terminal size
        term_width, term_height = self.terminal.get_terminal_size()
        
        # Calculate board display area
        board_width = board.width * 2 + 3  # 2 chars per cell + borders
        board_height = board.height + 2    # +2 for top/bottom borders
        
        # Calculate starting position for centering
        start_x = max(1, (term_width - board_width) // 2)
        start_y = max(3, (term_height - board_height - 5) // 2)  # -5 for status area
        
        # Render status bar
        self._render_status(game_state, start_x, start_y - 2, board_width)
        
        # Render board
        self._render_board(board, game_state, start_x, start_y)
        
        # Render controls help
        self._render_controls(start_x, start_y + board_height + 1, board_width)
    
    def _render_status(self, game_state: GameState, x: int, y: int, width: int) -> None:
        """Render game status bar."""
        if game_state.current_difficulty is None:
            return
        
        elapsed_time = game_state.get_elapsed_time()
        remaining_mines = game_state.get_remaining_mines()
        status_text = game_state.status.value.upper()
        
        # Format time
        time_str = f"Time: {elapsed_time//60:02d}:{elapsed_time%60:02d}"
        mines_str = f"Mines: {remaining_mines:03d}"
        status_str = f"Status: {status_text}"
        
        # Create status line
        status_line = f"{time_str}  |  {mines_str}  |  {status_str}"
        
        # Center the status line
        status_x = x + (width - len(status_line)) // 2
        
        # Render with border
        border_line = self.borders['horizontal'] * width
        self.terminal.write_at(x, y, self.borders['top_left'] + border_line + self.borders['top_right'])
        self.terminal.write_at(x, y + 1, self.borders['vertical'] + " " * width + self.borders['vertical'])
        self.terminal.write_at(status_x, y + 1, status_line)
        self.terminal.write_at(x, y + 2, self.borders['bottom_left'] + border_line + self.borders['bottom_right'])
    
    def _render_board(self, board: GameBoard, game_state: GameState, start_x: int, start_y: int) -> None:
        """Render the game board with borders."""
        # Top border
        self._render_top_border(board, start_x, start_y)
        
        # Board rows
        for y in range(board.height):
            self._render_board_row(board, game_state, y, start_x, start_y + y + 1)
        
        # Bottom border
        self._render_bottom_border(board, start_x, start_y + board.height + 1)
    
    def _render_top_border(self, board: GameBoard, start_x: int, y: int) -> None:
        """Render top border with column labels."""
        # Column labels (A, B, C, ...)
        labels = "  "
        for x in range(board.width):
            labels += chr(ord('A') + x) + " "
        
        self.terminal.write_at(start_x, y, labels)
    
    def _render_bottom_border(self, board: GameBoard, start_x: int, y: int) -> None:
        """Render bottom border."""
        border = "  " + self.borders['horizontal'] * (board.width * 2 - 1)
        self.terminal.write_at(start_x, y, border)
    
    def _render_board_row(self, board: GameBoard, game_state: GameState, row: int, start_x: int, y: int) -> None:
        """Render a single board row."""
        # Row label (1, 2, 3, ...)
        row_label = f"{row + 1:2d}"
        self.terminal.write_at(start_x, y, row_label)
        
        # Row cells
        for col in range(board.width):
            cell_x = start_x + 2 + col * 2
            self._render_cell(board, game_state, col, row, cell_x, y)
    
    def _render_cell(self, board: GameBoard, game_state: GameState, x: int, y: int, render_x: int, render_y: int) -> None:
        """Render a single cell."""
        cell = board.get_cell(x, y)
        if cell is None:
            return
        
        # Determine cursor highlighting
        is_cursor = (game_state.cursor_x == x and game_state.cursor_y == y)
        
        # Determine cell display character and color
        char, color = self._get_cell_display(cell, is_cursor, game_state)
        
        # Set color if specified
        if color:
            self.terminal.set_color(color)
        
        # Apply cursor highlighting
        if is_cursor and not color:
            self.terminal.set_color(self.terminal.Colors.INVERSE)
        
        self.terminal.write_at(render_x, render_y, char)
        
        # Reset color
        self.terminal.reset_color()
    
    def _get_cell_display(self, cell: Cell, is_cursor: bool, game_state: GameState) -> tuple[str, Optional[str]]:
        """
        Get display character and color for a cell.
        
        Returns:
            Tuple of (character, color_code)
        """
        # Flagged cells
        if cell.is_flagged:
            return self.chars['flag'], self.terminal.Colors.YELLOW
        
        # Hidden cells
        if not cell.is_revealed:
            if is_cursor:
                return self.chars['cursor_hidden'], None
            else:
                return self.chars['hidden'], None
        
        # Revealed cells
        if cell.has_mine:
            # Show mines (game over state)
            return self.chars['mine'], self.terminal.Colors.RED
        
        if cell.adjacent_mines == 0:
            # Empty cell
            return self.chars['revealed_empty'], None
        else:
            # Numbered cell
            number = str(cell.adjacent_mines)
            color = self.terminal.get_number_color(cell.adjacent_mines)
            return number, color
    
    def _render_controls(self, x: int, y: int, width: int) -> None:
        """Render control instructions."""
        controls = "Controls: ↑↓←→ Move | SPACE Reveal | Q Flag | ESC Exit"
        
        # Center the controls text
        controls_x = x + (width - len(controls)) // 2
        self.terminal.write_at(controls_x, y, controls)
    
    def check_board_size(self, board: GameBoard) -> tuple[bool, str]:
        """
        Check if terminal size is adequate for board display.
        
        Returns:
            Tuple of (is_adequate, error_message)
        """
        term_width, term_height = self.terminal.get_terminal_size()
        
        # Calculate required space
        required_width = board.width * 2 + 10  # +10 for margins and borders
        required_height = board.height + 10    # +10 for status and margins
        
        if term_width < required_width or term_height < required_height:
            error_msg = (
                f"Terminal too small for {board.width}x{board.height} board. "
                f"Need at least {required_width}x{required_height}, "
                f"got {term_width}x{term_height}"
            )
            return False, error_msg
        
        return True, ""
    
    def render_game_over_board(self, board: GameBoard, game_state: GameState) -> None:
        """Render board in game over state (shows all mines)."""
        # Same as regular render, but mines will be revealed
        self.render_game(board, game_state)
        
        # Add game over overlay if desired
        if game_state.status.value in ['won', 'lost']:
            term_width, term_height = self.terminal.get_terminal_size()
            
            if game_state.status.value == 'won':
                message = "🎉 VICTORY! 🎉"
                color = self.terminal.Colors.GREEN
            else:
                message = "💥 BOOM! 💥"
                color = self.terminal.Colors.RED
            
            # Display message at bottom
            message_x = (term_width - len(message)) // 2
            self.terminal.set_color(color + self.terminal.Colors.BOLD)
            self.terminal.write_at(message_x, term_height - 3, message)
            self.terminal.reset_color()
