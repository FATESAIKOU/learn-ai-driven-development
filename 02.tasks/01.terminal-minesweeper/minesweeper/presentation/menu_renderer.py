"""Menu rendering for minesweeper game."""

from typing import List
from ..infrastructure import TerminalManager
from ..models import DEFAULT_DIFFICULTIES


class MenuRenderer:
    """Renders the main menu and difficulty selection."""
    
    def __init__(self, terminal: TerminalManager):
        """Initialize menu renderer."""
        self.terminal = terminal
        self.title = "TERMINAL MINESWEEPER"
        self.instructions = [
            "Use ↑↓ to navigate, SPACE to select",
            "ESC to exit"
        ]
    
    def render_main_menu(self, selected_index: int = 0) -> None:
        """Render the main menu with difficulty selection."""
        self.terminal.clear_screen()
        
        # Get terminal size for centering
        term_width, term_height = self.terminal.get_terminal_size()
        
        # Menu content
        menu_options = self._get_menu_options()
        menu_height = len(menu_options) + len(self.instructions) + 6  # padding
        
        # Calculate starting position for vertical centering
        start_y = max(2, (term_height - menu_height) // 2)
        
        # Render title
        self._render_title(term_width, start_y)
        
        # Render menu options
        self._render_menu_options(menu_options, selected_index, term_width, start_y + 4)
        
        # Render instructions
        self._render_instructions(term_width, start_y + 4 + len(menu_options) + 2)
    
    def _render_title(self, term_width: int, y: int) -> None:
        """Render the game title."""
        # Title box
        title_width = len(self.title) + 4
        title_x = (term_width - title_width) // 2
        
        self.terminal.write_at(title_x, y, "╔" + "═" * (title_width - 2) + "╗")
        self.terminal.write_at(title_x, y + 1, f"║ {self.title} ║")
        self.terminal.write_at(title_x, y + 2, "╚" + "═" * (title_width - 2) + "╝")
    
    def _render_menu_options(self, options: List[str], selected_index: int, term_width: int, start_y: int) -> None:
        """Render menu options with selection highlighting."""
        max_option_width = max(len(option) for option in options) + 20  # padding for description
        menu_x = (term_width - max_option_width) // 2
        
        for i, option in enumerate(options):
            y = start_y + i
            
            # Prepare option text
            if i < len(DEFAULT_DIFFICULTIES):
                difficulty = DEFAULT_DIFFICULTIES[i]
                option_text = f"{option:<12} ({difficulty.width}x{difficulty.height}, {difficulty.mine_count} mines)"
            else:
                option_text = option
            
            # Highlight selected option
            if i == selected_index:
                self.terminal.set_color(self.terminal.Colors.INVERSE)
                prefix = "> "
            else:
                prefix = "  "
            
            self.terminal.write_at(menu_x, y, f"{prefix}{option_text}")
            
            if i == selected_index:
                self.terminal.reset_color()
    
    def _render_instructions(self, term_width: int, start_y: int) -> None:
        """Render instruction text."""
        for i, instruction in enumerate(self.instructions):
            instruction_x = (term_width - len(instruction)) // 2
            self.terminal.write_at(instruction_x, start_y + i, instruction)
    
    def _get_menu_options(self) -> List[str]:
        """Get list of menu options."""
        options = [diff.name for diff in DEFAULT_DIFFICULTIES]
        options.append("Exit")
        return options
    
    def render_game_over_menu(self, is_win: bool, elapsed_time: int, selected_index: int = 0) -> None:
        """Render game over screen with options."""
        self.terminal.clear_screen()
        
        # Get terminal size for centering
        term_width, term_height = self.terminal.get_terminal_size()
        
        # Game over message
        if is_win:
            title = "YOU WIN!"
            self.terminal.set_color(self.terminal.Colors.GREEN)
        else:
            title = "GAME OVER"
            self.terminal.set_color(self.terminal.Colors.RED)
        
        # Calculate positions
        start_y = (term_height - 10) // 2
        
        # Render title
        title_width = len(title) + 4
        title_x = (term_width - title_width) // 2
        
        self.terminal.write_at(title_x, start_y, "╔" + "═" * (title_width - 2) + "╗")
        self.terminal.write_at(title_x, start_y + 1, f"║ {title} ║")
        self.terminal.write_at(title_x, start_y + 2, "╚" + "═" * (title_width - 2) + "╝")
        
        self.terminal.reset_color()
        
        # Time display
        time_text = f"Time: {elapsed_time // 60:02d}:{elapsed_time % 60:02d}"
        time_x = (term_width - len(time_text)) // 2
        self.terminal.write_at(time_x, start_y + 4, time_text)
        
        # Result message
        if is_win:
            message = "All mines found!"
        else:
            message = "You hit a mine!"
        
        message_x = (term_width - len(message)) // 2
        self.terminal.write_at(message_x, start_y + 5, message)
        
        # Menu options
        options = ["Play Again", "Main Menu", "Exit"]
        for i, option in enumerate(options):
            y = start_y + 7 + i
            
            if i == selected_index:
                self.terminal.set_color(self.terminal.Colors.INVERSE)
                prefix = "> "
            else:
                prefix = "  "
            
            option_x = (term_width - len(option) - 2) // 2
            self.terminal.write_at(option_x, y, f"{prefix}{option}")
            
            if i == selected_index:
                self.terminal.reset_color()
        
        # Instructions
        instruction = "Use ↑↓ to navigate, SPACE to select"
        instruction_x = (term_width - len(instruction)) // 2
        self.terminal.write_at(instruction_x, start_y + 11, instruction)
    
    def check_terminal_size(self) -> tuple[bool, str]:
        """
        Check if terminal size is adequate for menu display.
        
        Returns:
            Tuple of (is_adequate, error_message)
        """
        width, height = self.terminal.get_terminal_size()
        min_width = 60
        min_height = 20
        
        if width < min_width or height < min_height:
            error_msg = f"Terminal too small. Need at least {min_width}x{min_height}, got {width}x{height}"
            return False, error_msg
        
        return True, ""
