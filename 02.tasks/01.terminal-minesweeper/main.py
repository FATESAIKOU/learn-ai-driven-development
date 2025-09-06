#!/usr/bin/env python3
"""
Terminal Minesweeper Game

A keyboard-controlled minesweeper game for the terminal.
Use arrow keys to navigate, space to reveal, Q to flag, ESC to exit.
"""

import sys
import time
from typing import Optional

from minesweeper.models import GameStatus, InputCommand
from minesweeper.infrastructure import TerminalManager, InputHandler
from minesweeper.logic import GameController
from minesweeper.presentation import MenuRenderer, GameRenderer


class MinesweeperApp:
    """Main application class for Terminal Minesweeper."""
    
    def __init__(self):
        """Initialize the application."""
        self.terminal = TerminalManager()
        self.input_handler = InputHandler()
        self.game_controller = GameController()
        self.menu_renderer = MenuRenderer(self.terminal)
        self.game_renderer = GameRenderer(self.terminal)
        
        self.running = True
        self.last_render_time = 0.0
        self.render_interval = 0.1  # Limit rendering to 10 FPS
    
    def run(self) -> int:
        """
        Run the main application loop.
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Check terminal capabilities
            if not self._check_requirements():
                return 1
            
            # Setup terminal
            self.terminal.setup()
            self.input_handler.setup()
            
            # Main game loop
            self._main_loop()
            
        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            pass
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        finally:
            # Always cleanup terminal and input
            self.input_handler.cleanup()
            self.terminal.cleanup()
        
        return 0
    
    def _check_requirements(self) -> bool:
        """Check if terminal meets minimum requirements."""
        # Check terminal size for menu
        is_adequate, error_msg = self.menu_renderer.check_terminal_size()
        if not is_adequate:
            print(f"Terminal Error: {error_msg}", file=sys.stderr)
            print("Please resize your terminal and try again.", file=sys.stderr)
            return False
        
        return True
    
    def _main_loop(self) -> None:
        """Main application loop."""
        # Initial render
        self._render_current_state()
        
        while self.running:
            # Get user input
            command = self.input_handler.get_command(timeout=0.1)
            
            # Process command based on current state
            if command != InputCommand.UNKNOWN:
                self._process_command(command)
            
            # Render if enough time has passed
            current_time = time.time()
            if current_time - self.last_render_time >= self.render_interval:
                self._render_current_state()
                self.last_render_time = current_time
            
            # Check if we should exit
            if self.game_controller.game_state.status == GameStatus.EXITED:
                self.running = False
    
    def _process_command(self, command: InputCommand) -> None:
        """Process a user command based on current game state."""
        status = self.game_controller.game_state.status
        
        if status == GameStatus.MENU:
            self.game_controller.process_menu_command(command)
            
        elif status == GameStatus.PLAYING:
            self.game_controller.process_game_command(command)
            
        elif status in [GameStatus.WON, GameStatus.LOST]:
            # For now, any key returns to menu
            if command in [InputCommand.SELECT, InputCommand.EXIT]:
                self.game_controller.game_state.status = GameStatus.MENU
                self.game_controller.game_state.selected_menu_index = 0
    
    def _render_current_state(self) -> None:
        """Render the current game state."""
        status = self.game_controller.game_state.status
        
        try:
            if status == GameStatus.MENU:
                self._render_menu()
                
            elif status == GameStatus.PLAYING:
                self._render_game()
                
            elif status in [GameStatus.WON, GameStatus.LOST]:
                self._render_game_over()
                
        except Exception as e:
            # If rendering fails, try to show error message
            self.terminal.clear_screen()
            self.terminal.write_at(1, 1, f"Render Error: {e}")
            self.terminal.write_at(1, 2, "Press ESC to exit")
    
    def _render_menu(self) -> None:
        """Render the main menu."""
        selected_index = self.game_controller.game_state.selected_menu_index
        self.menu_renderer.render_main_menu(selected_index)
    
    def _render_game(self) -> None:
        """Render the game board."""
        board = self.game_controller.board
        game_state = self.game_controller.game_state
        
        if board is None:
            return
        
        # Check if terminal is large enough for this board
        is_adequate, error_msg = self.game_renderer.check_board_size(board)
        if not is_adequate:
            self.terminal.clear_screen()
            self.terminal.write_at(1, 1, "Terminal Size Error:")
            self.terminal.write_at(1, 2, error_msg)
            self.terminal.write_at(1, 4, "Please resize terminal or choose smaller difficulty")
            self.terminal.write_at(1, 5, "Press ESC to return to menu")
            return
        
        self.game_renderer.render_game(board, game_state)
    
    def _render_game_over(self) -> None:
        """Render game over screen."""
        is_win = self.game_controller.game_state.status == GameStatus.WON
        elapsed_time = self.game_controller.game_state.get_elapsed_time()
        
        # Show final board state briefly, then show game over menu
        if hasattr(self, '_game_over_start_time'):
            time_since_game_over = time.time() - self._game_over_start_time
            if time_since_game_over > 2.0:  # Show board for 2 seconds
                self.menu_renderer.render_game_over_menu(is_win, elapsed_time)
            else:
                # Show final board state
                if self.game_controller.board:
                    self.game_renderer.render_game_over_board(
                        self.game_controller.board, 
                        self.game_controller.game_state
                    )
        else:
            # First time rendering game over
            self._game_over_start_time = time.time()
            if self.game_controller.board:
                self.game_renderer.render_game_over_board(
                    self.game_controller.board,
                    self.game_controller.game_state
                )


def main() -> int:
    """Main entry point."""
    app = MinesweeperApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
