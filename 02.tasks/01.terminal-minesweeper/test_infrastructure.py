#!/usr/bin/env python3
"""Test basic infrastructure components."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from minesweeper.models import Cell, Difficulty, GameState, GameStatus, DEFAULT_DIFFICULTIES
from minesweeper.infrastructure import TerminalManager, InputHandler


def test_models():
    """Test data models."""
    print("Testing data models...")
    
    # Test Cell
    cell = Cell()
    assert not cell.has_mine
    assert not cell.is_revealed
    assert not cell.is_flagged
    assert cell.can_reveal()
    assert cell.can_flag()
    
    # Test Difficulty
    beginner = DEFAULT_DIFFICULTIES[0]
    assert beginner.name == "Beginner"
    assert beginner.width == 9
    assert beginner.height == 9
    assert beginner.mine_count == 10
    assert beginner.is_valid()
    
    # Test GameState
    game_state = GameState()
    assert game_state.status == GameStatus.MENU
    assert game_state.cursor_x == 0
    assert game_state.cursor_y == 0
    
    print("✓ Data models test passed")


def test_terminal_manager():
    """Test terminal manager."""
    print("Testing terminal manager...")
    
    tm = TerminalManager()
    assert not tm.is_setup
    
    # Test color support detection
    supports_color = tm._supports_color
    print(f"  Color support: {supports_color}")
    
    # Test terminal size
    width, height = tm.get_terminal_size()
    print(f"  Terminal size: {width}x{height}")
    
    # Test size adequacy
    adequate = tm.is_size_adequate(80, 24)
    print(f"  Size adequate (80x24): {adequate}")
    
    print("✓ Terminal manager test passed")


def test_input_handler():
    """Test input handler."""
    print("Testing input handler...")
    
    ih = InputHandler()
    assert isinstance(ih.key_mapping, dict)
    assert len(ih.key_mapping) > 0
    
    # Test key mapping
    from minesweeper.models import InputCommand
    assert ih.key_mapping[' '] == InputCommand.SELECT
    assert ih.key_mapping['q'] == InputCommand.FLAG
    assert ih.key_mapping['\x1b'] == InputCommand.EXIT
    
    print("✓ Input handler test passed")


def main():
    """Run all tests."""
    print("Running infrastructure tests...\n")
    
    try:
        test_models()
        test_terminal_manager()
        test_input_handler()
        print("\n✅ All tests passed!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
