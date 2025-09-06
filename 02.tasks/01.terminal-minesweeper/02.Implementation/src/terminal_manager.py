"""
Terminal management utilities for cross-platform terminal control.

This module handles terminal setup, cleanup, and display operations.
"""

import os
import sys
import termios
import tty
from typing import Optional


class TerminalManager:
    """Manages terminal display and cursor operations."""
    
    def __init__(self):
        self.original_settings: Optional[list] = None
        self.is_setup = False
    
    def setup_terminal(self) -> None:
        """Setup terminal for game display."""
        if self.is_setup:
            return
            
        try:
            # Save original terminal settings
            self.original_settings = termios.tcgetattr(sys.stdin.fileno())
            
            # Set terminal to raw mode for immediate key detection
            tty.setraw(sys.stdin.fileno())
            
            # Hide cursor and setup alternate screen buffer
            self._write_escape_sequence('\033[?25l')  # Hide cursor
            self._write_escape_sequence('\033[?1049h')  # Use alternate screen buffer
            
            self.is_setup = True
            
        except Exception as e:
            print(f"Warning: Could not setup terminal properly: {e}")
            # Continue without raw mode if setup fails
    
    def restore_terminal(self) -> None:
        """Restore original terminal settings."""
        if not self.is_setup:
            return
            
        try:
            # Restore cursor and screen buffer
            self._write_escape_sequence('\033[?25h')  # Show cursor
            self._write_escape_sequence('\033[?1049l')  # Restore normal screen buffer
            
            # Restore original terminal settings
            if self.original_settings:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.original_settings)
                
            self.is_setup = False
            
        except Exception as e:
            print(f"Warning: Could not restore terminal properly: {e}")
    
    def clear_screen(self) -> None:
        """Clear terminal screen."""
        self._write_escape_sequence('\033[2J\033[H')
    
    def move_cursor(self, row: int, col: int) -> None:
        """Move cursor to specific position (1-based coordinates)."""
        self._write_escape_sequence(f'\033[{row};{col}H')
    
    def set_color(self, color_code: str) -> None:
        """Set text color using ANSI escape code."""
        self._write_escape_sequence(color_code)
    
    def reset_color(self) -> None:
        """Reset text color to default."""
        self._write_escape_sequence('\033[0m')
    
    def get_terminal_size(self) -> tuple[int, int]:
        """Get terminal size as (width, height)."""
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            # Default size if detection fails
            return 80, 24
    
    def write_at(self, row: int, col: int, text: str, color: str = '') -> None:
        """Write text at specific position with optional color."""
        self.move_cursor(row, col)
        if color:
            self.set_color(color)
        self._write_text(text)
        if color:
            self.reset_color()
    
    def center_text(self, row: int, text: str, color: str = '') -> None:
        """Write centered text on specified row."""
        terminal_width, _ = self.get_terminal_size()
        col = max(1, (terminal_width - len(text)) // 2 + 1)
        self.write_at(row, col, text, color)
    
    def draw_box(self, top_row: int, left_col: int, width: int, height: int, 
                 color: str = '') -> None:
        """Draw a box using Unicode box drawing characters."""
        if color:
            self.set_color(color)
        
        # Top border
        self.move_cursor(top_row, left_col)
        self._write_text('╔' + '═' * (width - 2) + '╗')
        
        # Side borders
        for i in range(1, height - 1):
            self.move_cursor(top_row + i, left_col)
            self._write_text('║')
            self.move_cursor(top_row + i, left_col + width - 1)
            self._write_text('║')
        
        # Bottom border
        self.move_cursor(top_row + height - 1, left_col)
        self._write_text('╚' + '═' * (width - 2) + '╝')
        
        if color:
            self.reset_color()
    
    def draw_horizontal_line(self, row: int, left_col: int, width: int, 
                           char: str = '═', color: str = '') -> None:
        """Draw a horizontal line."""
        if color:
            self.set_color(color)
        self.move_cursor(row, left_col)
        self._write_text(char * width)
        if color:
            self.reset_color()
    
    def fill_area(self, top_row: int, left_col: int, width: int, height: int, 
                  char: str = ' ', color: str = '') -> None:
        """Fill an area with specified character."""
        if color:
            self.set_color(color)
        
        for i in range(height):
            self.move_cursor(top_row + i, left_col)
            self._write_text(char * width)
        
        if color:
            self.reset_color()
    
    def _write_escape_sequence(self, sequence: str) -> None:
        """Write ANSI escape sequence to stdout."""
        sys.stdout.write(sequence)
        sys.stdout.flush()
    
    def _write_text(self, text: str) -> None:
        """Write text to stdout."""
        sys.stdout.write(text)
        sys.stdout.flush()
    
    def __enter__(self):
        """Context manager entry."""
        self.setup_terminal()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.restore_terminal()
