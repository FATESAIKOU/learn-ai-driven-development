"""Input handling for the Minesweeper game.

This module provides cross-platform input handling with proper key detection.
"""

import sys
import signal
import termios
import tty
from typing import Optional

from ..models.game_models import InputCommand


class InputHandler:
    """Handle keyboard input for the terminal-based Minesweeper game."""
    
    def __init__(self):
        """Initialize the input handler."""
        self.old_settings = None
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Setup signal handlers for clean exit."""
        def signal_handler(signum, frame):
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def setup(self):
        """Setup terminal for character input."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            # Use cbreak mode instead of raw - allows Ctrl+C to work
            tty.setcbreak(sys.stdin.fileno())
    
    def cleanup(self):
        """Restore terminal settings."""
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    
    def getch(self) -> Optional[str]:
        """Get a single character from stdin."""
        try:
            return sys.stdin.read(1)
        except KeyboardInterrupt:
            return '\x03'  # Ctrl+C
        except Exception:
            return None
    
    def get_key(self) -> Optional[str]:
        """Get a key press from the user with proper arrow key detection.
        
        Returns:
            The key pressed as a string, or None if no key available.
        """
        if not sys.stdin.isatty():
            return None
        
        try:
            char1 = self.getch()
            if char1 == '\x1b':  # ESC
                char2 = self.getch()
                if char2 == '[':
                    char3 = self.getch()
                    if char3 in 'ABCD':
                        return f'\x1b[{char3}'
                    else:
                        # Not an arrow key, return ESC
                        return '\x1b'
                else:
                    # ESC followed by something else
                    return '\x1b'
            else:
                return char1
        except Exception:
            return None
    
    def get_command(self, timeout: float = 0.1) -> InputCommand:
        """Get a game command from user input.
        
        Args:
            timeout: Not used in this implementation but kept for compatibility
        
        Returns:
            A InputCommand enum value, UNKNOWN if no valid command.
        """
        key = self.get_key()
        if key is None:
            return InputCommand.UNKNOWN
        
        # Map keys to commands
        key_map = {
            '\x1b[A': InputCommand.MOVE_UP,      # Up arrow
            '\x1b[B': InputCommand.MOVE_DOWN,    # Down arrow
            '\x1b[D': InputCommand.MOVE_LEFT,    # Left arrow
            '\x1b[C': InputCommand.MOVE_RIGHT,   # Right arrow
            ' ': InputCommand.SELECT,            # Space
            'q': InputCommand.EXIT,              # Q key
            'Q': InputCommand.EXIT,              # Q key (uppercase)
            '\x1b': InputCommand.EXIT,           # ESC key
            '\x03': InputCommand.EXIT,           # Ctrl+C
        }
        
        return key_map.get(key, InputCommand.UNKNOWN)
