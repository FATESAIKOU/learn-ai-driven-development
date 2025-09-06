#!/usr/bin/env python3
"""
Quick test for basic components to ensure they work correctly.
"""

import sys
import time
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from models import Cell, Difficulty, DIFFICULTIES, Colors
from terminal_manager import TerminalManager
from input_handler import InputHandler, InputCommand


def test_models():
    """Test basic model functionality."""
    print("Testing models...")
    
    # Test Cell
    cell = Cell()
    assert cell.can_reveal() == True
    cell.is_flagged = True
    assert cell.can_reveal() == False
    assert cell.get_display_char() == 'F'
    
    # Test Difficulty
    beginner = DIFFICULTIES['Beginner']
    assert beginner.is_valid() == True
    assert beginner.get_description() == "Beginner (9x9, 10 mines)"
    
    print("✓ Models test passed")


def test_terminal_manager():
    """Test terminal manager functionality."""
    print("Testing terminal manager...")
    
    with TerminalManager() as tm:
        tm.clear_screen()
        tm.write_at(1, 1, "Terminal Manager Test", Colors.BRIGHT_GREEN)
        tm.center_text(3, "This text should be centered", Colors.BRIGHT_CYAN)
        tm.draw_box(5, 10, 30, 5, Colors.BRIGHT_WHITE)
        tm.write_at(7, 12, "Box content test", Colors.YELLOW)
        
        tm.write_at(12, 1, "Press any key to continue...", Colors.BRIGHT_YELLOW)
        
        # Wait for input
        input_handler = InputHandler()
        input_handler.get_input_blocking()
    
    print("✓ Terminal manager test passed")


def test_input_handler():
    """Test input handler functionality."""
    print("Testing input handler...")
    
    with TerminalManager() as tm:
        tm.clear_screen()
        tm.center_text(2, "INPUT HANDLER TEST", Colors.BRIGHT_GREEN)
        tm.center_text(4, "Try different keys:", Colors.WHITE)
        
        controls = [
            "Arrow keys: Move commands",
            "Space: Select command", 
            "Q: Flag command",
            "ESC: Exit command",
            "Other keys: Invalid command"
        ]
        
        for i, control in enumerate(controls):
            tm.write_at(6 + i, 5, control, Colors.CYAN)
        
        tm.write_at(13, 5, "Press ESC to exit test...", Colors.BRIGHT_YELLOW)
        
        input_handler = InputHandler()
        row = 15
        
        while True:
            command = input_handler.get_input_blocking()
            
            if command == InputCommand.EXIT:
                break
            
            # Display the command
            tm.write_at(row, 5, f"Command: {command.value:<15}", Colors.WHITE)
            row += 1
            if row > 20:
                row = 15
                tm.fill_area(15, 5, 50, 6)  # Clear command display area
    
    print("✓ Input handler test passed")


def main():
    """Run all tests."""
    try:
        test_models()
        test_terminal_manager() 
        test_input_handler()
        print("\n✓ All basic component tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
