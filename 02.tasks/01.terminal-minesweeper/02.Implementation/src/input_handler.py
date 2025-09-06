"""
Input handling for keyboard events and command mapping.

This module handles keyboard input capture and converts key presses to game commands.
"""

import sys
import select
import termios
import tty
from typing import Optional

from models import InputCommand


class InputHandler:
    """Handles keyboard input and converts to commands."""
    
    def __init__(self):
        self.key_mappings = {
            # Arrow keys (ANSI escape sequences)
            '\x1b[A': InputCommand.MOVE_UP,
            '\x1b[B': InputCommand.MOVE_DOWN,
            '\x1b[C': InputCommand.MOVE_RIGHT,
            '\x1b[D': InputCommand.MOVE_LEFT,
            
            # Action keys
            ' ': InputCommand.SELECT,           # Space
            'q': InputCommand.FLAG,             # Q key
            'Q': InputCommand.FLAG,             # Q key (uppercase)
            '\x1b': InputCommand.EXIT,          # ESC key
            '\x03': InputCommand.EXIT,          # Ctrl+C
            '\x04': InputCommand.EXIT,          # Ctrl+D
        }
        
        # Additional key variations for better compatibility
        self.alternative_mappings = {
            'w': InputCommand.MOVE_UP,          # WASD alternative
            's': InputCommand.MOVE_DOWN,
            'a': InputCommand.MOVE_LEFT,
            'd': InputCommand.MOVE_RIGHT,
            'W': InputCommand.MOVE_UP,
            'S': InputCommand.MOVE_DOWN,
            'A': InputCommand.MOVE_LEFT,
            'D': InputCommand.MOVE_RIGHT,
            '\r': InputCommand.SELECT,          # Enter key
            '\n': InputCommand.SELECT,          # Newline
        }
        
        self.enable_alternatives = False  # Can be enabled for accessibility
    
    def get_input(self, timeout: float = 0.1) -> InputCommand:
        """
        Get and convert keyboard input to command.
        
        Args:
            timeout: Maximum time to wait for input in seconds
            
        Returns:
            InputCommand representing the user's action
        """
        try:
            key = self._read_key_with_timeout(timeout)
            if key is None:
                return InputCommand.INVALID
                
            # Check primary mappings first
            if key in self.key_mappings:
                return self.key_mappings[key]
            
            # Check alternative mappings if enabled
            if self.enable_alternatives and key in self.alternative_mappings:
                return self.alternative_mappings[key]
            
            return InputCommand.INVALID
            
        except Exception:
            return InputCommand.INVALID
    
    def get_input_blocking(self) -> InputCommand:
        """Get input without timeout (blocking)."""
        try:
            key = self._read_key()
            
            if key in self.key_mappings:
                return self.key_mappings[key]
            
            if self.enable_alternatives and key in self.alternative_mappings:
                return self.alternative_mappings[key]
            
            return InputCommand.INVALID
            
        except Exception:
            return InputCommand.INVALID
    
    def _read_key(self) -> str:
        """Read a single key from stdin (blocking)."""
        # Read first character
        char = sys.stdin.read(1)
        
        # Handle escape sequences (multi-character keys like arrow keys)
        if char == '\x1b':  # ESC character
            # Check if this is just ESC key or start of escape sequence
            if self._has_more_input():
                # Read the rest of the escape sequence
                char += sys.stdin.read(1)  # Should be '['
                if char == '\x1b[':
                    char += sys.stdin.read(1)  # Direction character
        
        return char
    
    def _read_key_with_timeout(self, timeout: float) -> Optional[str]:
        """Read a key with timeout using select."""
        # Check if input is available
        if select.select([sys.stdin], [], [], timeout)[0]:
            return self._read_key()
        return None
    
    def _has_more_input(self) -> bool:
        """Check if more input is available without blocking."""
        return select.select([sys.stdin], [], [], 0)[0]
    
    def flush_input(self) -> None:
        """Flush any pending input from the buffer."""
        try:
            while self._has_more_input():
                sys.stdin.read(1)
        except Exception:
            pass
    
    def enable_alternative_keys(self, enable: bool = True) -> None:
        """Enable or disable alternative key mappings (WASD, Enter)."""
        self.enable_alternatives = enable
    
    def add_custom_mapping(self, key: str, command: InputCommand) -> None:
        """Add custom key mapping."""
        self.key_mappings[key] = command
    
    def get_key_for_command(self, command: InputCommand) -> Optional[str]:
        """Get the primary key for a given command."""
        for key, cmd in self.key_mappings.items():
            if cmd == command:
                return key
        return None
    
    def get_command_description(self, command: InputCommand) -> str:
        """Get human-readable description of command."""
        descriptions = {
            InputCommand.MOVE_UP: "↑ Move Up",
            InputCommand.MOVE_DOWN: "↓ Move Down", 
            InputCommand.MOVE_LEFT: "← Move Left",
            InputCommand.MOVE_RIGHT: "→ Move Right",
            InputCommand.SELECT: "SPACE Select/Reveal",
            InputCommand.FLAG: "Q Flag/Unflag",
            InputCommand.EXIT: "ESC Exit",
        }
        return descriptions.get(command, "Unknown Command")
    
    def get_controls_help(self) -> list[str]:
        """Get list of control descriptions for display."""
        return [
            "↑↓←→ Move cursor",
            "SPACE Reveal cell",
            "Q Flag/Unflag cell", 
            "ESC Exit game"
        ]


# Global input handler instance for convenience
input_handler = InputHandler()
