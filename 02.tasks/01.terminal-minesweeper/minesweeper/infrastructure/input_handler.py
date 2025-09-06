"""Input handling for keyboard events."""

import sys
import select
import signal
from typing import Optional
from ..models import InputCommand


class InputHandler:
    """Handles keyboard input and converts to game commands."""
    
    def __init__(self):
        """Initialize input handler."""
        self.key_mapping = {
            # Arrow keys (ANSI escape sequences)
            '\x1b[A': InputCommand.MOVE_UP,
            '\x1b[B': InputCommand.MOVE_DOWN,
            '\x1b[C': InputCommand.MOVE_RIGHT,
            '\x1b[D': InputCommand.MOVE_LEFT,
            
            # Action keys
            ' ': InputCommand.SELECT,       # Space
            'q': InputCommand.FLAG,         # Q key
            'Q': InputCommand.FLAG,         # Q key (uppercase)
            '\x1b': InputCommand.EXIT,      # ESC key
            '\x03': InputCommand.EXIT,      # Ctrl+C
            '\x04': InputCommand.EXIT,      # Ctrl+D
        }
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum: int, frame) -> None:
        """Handle system signals for graceful exit."""
        # This will be caught by the main loop
        raise KeyboardInterrupt()
    
    def get_command(self, timeout: float = 0.1) -> InputCommand:
        """Get input command with timeout."""
        try:
            if self._has_input(timeout):
                key = self._read_key()
                command = self.key_mapping.get(key, InputCommand.UNKNOWN)
                return command
            return InputCommand.UNKNOWN
        except KeyboardInterrupt:
            return InputCommand.EXIT
        except Exception:
            # Handle any unexpected input errors
            return InputCommand.UNKNOWN
    
    def wait_for_command(self) -> InputCommand:
        """Wait indefinitely for a command (blocking)."""
        try:
            key = self._read_key_blocking()
            return self.key_mapping.get(key, InputCommand.UNKNOWN)
        except KeyboardInterrupt:
            return InputCommand.EXIT
        except Exception:
            return InputCommand.UNKNOWN
    
    def _has_input(self, timeout: float) -> bool:
        """Check if input is available within timeout."""
        if not hasattr(sys.stdin, 'isatty') or not sys.stdin.isatty():
            return False
        
        try:
            # Use select to check for input availability
            if sys.platform == 'win32':
                # Windows doesn't support select on stdin
                import msvcrt
                return msvcrt.kbhit()
            else:
                # Unix-like systems
                ready, _, _ = select.select([sys.stdin], [], [], timeout)
                return bool(ready)
        except Exception:
            return False
    
    def _read_key(self) -> str:
        """Read a key sequence from stdin."""
        try:
            if sys.platform == 'win32':
                import msvcrt
                key = msvcrt.getch().decode('utf-8')
                
                # Handle special keys on Windows
                if key == '\x00' or key == '\xe0':  # Special key prefix
                    key2 = msvcrt.getch().decode('utf-8')
                    # Convert Windows arrow keys to ANSI sequences
                    arrow_map = {
                        'H': '\x1b[A',  # Up
                        'P': '\x1b[B',  # Down
                        'M': '\x1b[C',  # Right
                        'K': '\x1b[D',  # Left
                    }
                    return arrow_map.get(key2, key + key2)
                
                return key
            else:
                # Unix-like systems
                key = sys.stdin.read(1)
                
                # Handle escape sequences
                if key == '\x1b':
                    if self._has_input(0.01):  # Very short timeout for escape sequences
                        key += sys.stdin.read(1)
                        if key == '\x1b[' and self._has_input(0.01):
                            key += sys.stdin.read(1)
                
                return key
        except Exception:
            return ''
    
    def _read_key_blocking(self) -> str:
        """Read a key sequence with no timeout (blocking)."""
        try:
            if sys.platform == 'win32':
                import msvcrt
                key = msvcrt.getch().decode('utf-8')
                
                # Handle special keys on Windows
                if key == '\x00' or key == '\xe0':
                    key2 = msvcrt.getch().decode('utf-8')
                    arrow_map = {
                        'H': '\x1b[A',  # Up
                        'P': '\x1b[B',  # Down
                        'M': '\x1b[C',  # Right
                        'K': '\x1b[D',  # Left
                    }
                    return arrow_map.get(key2, key + key2)
                
                return key
            else:
                # Unix-like systems
                key = sys.stdin.read(1)
                
                # Handle escape sequences
                if key == '\x1b':
                    # Wait a bit longer for escape sequences in blocking mode
                    if self._has_input(0.1):
                        key += sys.stdin.read(1)
                        if key == '\x1b[' and self._has_input(0.1):
                            key += sys.stdin.read(1)
                
                return key
        except Exception:
            return ''
    
    def flush_input(self) -> None:
        """Flush any pending input."""
        try:
            if sys.platform == 'win32':
                import msvcrt
                while msvcrt.kbhit():
                    msvcrt.getch()
            else:
                # Unix-like systems
                import termios
                termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            pass
