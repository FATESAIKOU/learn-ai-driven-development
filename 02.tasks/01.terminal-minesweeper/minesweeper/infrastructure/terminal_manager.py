"""Terminal management for cross-platform terminal control."""

import sys
import os
from typing import Optional


class TerminalManager:
    """Manages terminal display and cursor control."""
    
    # ANSI color codes
    class Colors:
        RESET = '\x1b[0m'
        BOLD = '\x1b[1m'
        INVERSE = '\x1b[7m'
        
        # Foreground colors
        BLACK = '\x1b[30m'
        RED = '\x1b[31m'
        GREEN = '\x1b[32m'
        YELLOW = '\x1b[33m'
        BLUE = '\x1b[34m'
        MAGENTA = '\x1b[35m'
        CYAN = '\x1b[36m'
        WHITE = '\x1b[37m'
        BRIGHT_WHITE = '\x1b[97m'
        
        # Background colors
        BG_BLACK = '\x1b[40m'
        BG_RED = '\x1b[41m'
        BG_GREEN = '\x1b[42m'
        BG_YELLOW = '\x1b[43m'
        BG_BLUE = '\x1b[44m'
        BG_MAGENTA = '\x1b[45m'
        BG_CYAN = '\x1b[46m'
        BG_WHITE = '\x1b[47m'
    
    def __init__(self):
        """Initialize terminal manager."""
        self.original_settings: Optional[list] = None
        self.is_setup = False
        self._supports_color = self._check_color_support()
    
    def _check_color_support(self) -> bool:
        """Check if terminal supports ANSI colors."""
        return (
            hasattr(sys.stdout, 'isatty') and 
            sys.stdout.isatty() and
            os.environ.get('TERM', '').lower() != 'dumb'
        )
    
    def setup(self) -> None:
        """Initialize terminal for game display."""
        if self.is_setup:
            return
        
        # Setup raw mode for immediate input (platform-specific)
        if hasattr(sys.stdin, 'isatty') and sys.stdin.isatty():
            try:
                if sys.platform != 'win32':
                    import termios
                    import tty
                    self.original_settings = termios.tcgetattr(sys.stdin)
                    tty.setcbreak(sys.stdin.fileno())
            except ImportError:
                # termios not available on Windows
                pass
        
        # Hide cursor and clear screen
        self.hide_cursor()
        self.clear_screen()
        self.is_setup = True
    
    def cleanup(self) -> None:
        """Restore terminal to original state."""
        if not self.is_setup:
            return
        
        self.show_cursor()
        self.reset_color()
        
        # Restore original terminal settings
        if self.original_settings is not None:
            try:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)
            except ImportError:
                pass
        
        self.is_setup = False
    
    def clear_screen(self) -> None:
        """Clear entire screen and move cursor to top-left."""
        if self._supports_color:
            sys.stdout.write('\x1b[2J\x1b[H')
        else:
            # Fallback for terminals without ANSI support
            os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.flush()
    
    def move_cursor(self, x: int, y: int) -> None:
        """Move cursor to specific position (1-indexed)."""
        if self._supports_color:
            sys.stdout.write(f'\x1b[{y};{x}H')
            sys.stdout.flush()
    
    def hide_cursor(self) -> None:
        """Hide terminal cursor."""
        if self._supports_color:
            sys.stdout.write('\x1b[?25l')
            sys.stdout.flush()
    
    def show_cursor(self) -> None:
        """Show terminal cursor."""
        if self._supports_color:
            sys.stdout.write('\x1b[?25h')
            sys.stdout.flush()
    
    def write(self, text: str) -> None:
        """Write text at current cursor position."""
        sys.stdout.write(text)
        sys.stdout.flush()
    
    def write_at(self, x: int, y: int, text: str) -> None:
        """Write text at specific position."""
        self.move_cursor(x, y)
        self.write(text)
    
    def set_color(self, color_code: str) -> None:
        """Set text color using ANSI color code."""
        if self._supports_color:
            sys.stdout.write(color_code)
            sys.stdout.flush()
    
    def reset_color(self) -> None:
        """Reset all color and style settings."""
        if self._supports_color:
            sys.stdout.write(self.Colors.RESET)
            sys.stdout.flush()
    
    def get_number_color(self, number: int) -> str:
        """Get color code for mine count numbers."""
        if not self._supports_color:
            return ''
        
        color_map = {
            1: self.Colors.BLUE,
            2: self.Colors.GREEN,
            3: self.Colors.RED,
            4: self.Colors.MAGENTA,
            5: self.Colors.YELLOW,
            6: self.Colors.CYAN,
            7: self.Colors.BLACK,
            8: self.Colors.WHITE,
        }
        return color_map.get(number, self.Colors.WHITE)
    
    def get_terminal_size(self) -> tuple[int, int]:
        """Get terminal size as (width, height)."""
        try:
            import shutil
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except Exception:
            # Fallback to default size
            return 80, 24
    
    def is_size_adequate(self, min_width: int, min_height: int) -> bool:
        """Check if terminal size is adequate for display."""
        width, height = self.get_terminal_size()
        return width >= min_width and height >= min_height
