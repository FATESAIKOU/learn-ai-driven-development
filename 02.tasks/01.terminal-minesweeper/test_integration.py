#!/usr/bin/env python3
"""Basic integration test for the minesweeper game."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    # Test model imports
    from minesweeper.models import Cell, Difficulty, GameState, GameStatus, InputCommand, DEFAULT_DIFFICULTIES
    
    # Test infrastructure imports
    from minesweeper.infrastructure import TerminalManager, InputHandler
    
    # Test logic imports
    from minesweeper.logic import MineGenerator, GameBoard, GameController
    
    # Test presentation imports
    from minesweeper.presentation import MenuRenderer, GameRenderer
    
    print("✓ All imports successful")


def test_basic_game_flow():
    """Test basic game initialization and flow."""
    print("Testing basic game flow...")
    
    from minesweeper.logic import GameController
    from minesweeper.models import InputCommand, GameStatus, DEFAULT_DIFFICULTIES
    
    # Create game controller
    controller = GameController()
    assert controller.game_state.status == GameStatus.MENU
    
    # Test menu navigation
    controller.process_menu_command(InputCommand.MOVE_DOWN)
    assert controller.game_state.selected_menu_index == 1
    
    # Start a game
    controller.process_menu_command(InputCommand.SELECT)  # Select Intermediate
    assert controller.game_state.status == GameStatus.PLAYING
    assert controller.board is not None
    
    # Test cursor movement
    old_x, old_y = controller.game_state.cursor_x, controller.game_state.cursor_y
    controller.process_game_command(InputCommand.MOVE_RIGHT)
    assert controller.game_state.cursor_x == old_x + 1 or controller.game_state.cursor_x == old_x
    
    print("✓ Basic game flow test passed")


def test_mine_generation():
    """Test mine generation logic."""
    print("Testing mine generation...")
    
    from minesweeper.logic import MineGenerator
    from minesweeper.models import Difficulty
    
    generator = MineGenerator(seed=42)  # Use seed for deterministic testing
    difficulty = Difficulty("Test", 5, 5, 3)
    
    # Generate mines
    mines = generator.generate_mines(difficulty, safe_position=(0, 0))
    
    # Validate mine placement
    assert len(mines) == 3
    assert (0, 0) not in mines  # Safe position should not have mine
    
    # Check all positions are valid
    for x, y in mines:
        assert 0 <= x < difficulty.width
        assert 0 <= y < difficulty.height
    
    print("✓ Mine generation test passed")


def test_board_operations():
    """Test game board operations."""
    print("Testing board operations...")
    
    from minesweeper.logic import GameBoard
    from minesweeper.models import Difficulty
    
    difficulty = Difficulty("Test", 5, 5, 3)
    board = GameBoard(difficulty)
    
    # Test initial state
    assert not board.is_initialized
    assert board.get_revealed_count() == 0
    assert board.get_flag_count() == 0
    
    # Test cell revelation
    success, hit_mine = board.reveal_cell(0, 0)
    assert success
    assert board.is_initialized  # Should initialize mines on first reveal
    
    # Print board state for debugging
    print(f"  Board state after first reveal:")
    print(f"  Revealed count: {board.get_revealed_count()}")
    for y in range(board.height):
        row = ""
        for x in range(board.width):
            cell = board.get_cell(x, y)
            if cell.is_revealed:
                if cell.adjacent_mines > 0:
                    row += str(cell.adjacent_mines)
                else:
                    row += " "
            else:
                row += "█"
        print(f"  {row}")
    
    # Find an unrevealed cell to test flagging
    unrevealed_pos = None
    for y in range(board.height):
        for x in range(board.width):
            cell = board.get_cell(x, y)
            if not cell.is_revealed:
                unrevealed_pos = (x, y)
                break
        if unrevealed_pos:
            break
    
    assert unrevealed_pos is not None, "No unrevealed cells found for flagging test"
    
    # Test flagging (on unrevealed cell)
    flag_x, flag_y = unrevealed_pos
    flag_success = board.toggle_flag(flag_x, flag_y)
    assert flag_success
    assert board.get_flag_count() == 1
    
    # Test unflagging
    unflag_success = board.toggle_flag(flag_x, flag_y)
    assert unflag_success
    assert board.get_flag_count() == 0
    
    print("✓ Board operations test passed")


def main():
    """Run all tests."""
    print("Running integration tests...\n")
    
    try:
        test_imports()
        test_basic_game_flow()
        test_mine_generation()
        test_board_operations()
        
        print("\n✅ All integration tests passed!")
        print("\nThe game is ready to play!")
        print("Run: uv run python main.py")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
