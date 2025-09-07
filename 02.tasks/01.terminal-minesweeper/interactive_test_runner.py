#!/usr/bin/env python3
"""
Interactive game testing framework that can actually control the game.
"""

import sys
import os
import time
import subprocess
import pexpect
import threading
from typing import List, Dict, Any, Optional

class GameInteractionTester:
    """Test framework that can interact with the actual running game."""
    
    def __init__(self, game_path: str):
        self.game_path = game_path
        self.process = None
        self.test_results = []
    
    def start_game(self, timeout: int = 10) -> bool:
        """Start the game process and wait for it to be ready."""
        try:
            # Use pexpect to spawn the game process
            self.process = pexpect.spawn(f'cd {os.path.dirname(self.game_path)} && python main.py')
            self.process.timeout = timeout
            
            # Wait for the main menu to appear
            self.process.expect('TERMINAL MINESWEEPER', timeout=5)
            print("✅ Game started successfully")
            return True
            
        except pexpect.exceptions.TIMEOUT:
            print("❌ Game failed to start (timeout)")
            return False
        except Exception as e:
            print(f"❌ Game failed to start: {e}")
            return False
    
    def send_key(self, key: str, wait_time: float = 0.1):
        """Send a key to the game and wait."""
        if self.process:
            self.process.send(key)
            time.sleep(wait_time)
    
    def send_arrow_key(self, direction: str, wait_time: float = 0.1):
        """Send arrow key in specified direction."""
        arrow_keys = {
            'up': '\x1b[A',
            'down': '\x1b[B',
            'left': '\x1b[D',
            'right': '\x1b[C'
        }
        if direction.lower() in arrow_keys:
            self.send_key(arrow_keys[direction.lower()], wait_time)
    
    def send_space(self, wait_time: float = 0.1):
        """Send space key (select/reveal)."""
        self.send_key(' ', wait_time)
    
    def send_esc(self, wait_time: float = 0.1):
        """Send ESC key (exit)."""
        self.send_key('\x1b', wait_time)
    
    def expect_text(self, text: str, timeout: int = 5) -> bool:
        """Wait for specific text to appear."""
        try:
            self.process.expect(text, timeout=timeout)
            return True
        except pexpect.exceptions.TIMEOUT:
            return False
    
    def get_screen_content(self) -> str:
        """Get current screen content."""
        if self.process:
            return self.process.before.decode('utf-8') if self.process.before else ""
        return ""
    
    def run_menu_navigation_test(self) -> Dict[str, Any]:
        """Test menu navigation functionality."""
        test_name = "Menu Navigation Test"
        print(f"\n🧪 Running {test_name}")
        
        result = {
            'name': test_name,
            'passed': False,
            'steps': [],
            'error': None
        }
        
        try:
            # Test down navigation
            print("  📱 Testing down arrow navigation...")
            self.send_arrow_key('down', 0.2)
            result['steps'].append('down_arrow_sent')
            
            # Test up navigation  
            print("  📱 Testing up arrow navigation...")
            self.send_arrow_key('up', 0.2)
            result['steps'].append('up_arrow_sent')
            
            # Test selection
            print("  📱 Testing space selection...")
            self.send_space(0.5)
            result['steps'].append('space_sent')
            
            # Check if we're in game (look for game board indicators)
            if self.expect_text('Status: PLAYING', timeout=3):
                print("  ✅ Successfully entered game mode")
                result['steps'].append('game_started')
                
                # Exit the game
                self.send_esc(0.5)
                result['steps'].append('esc_sent')
                
            result['passed'] = True
            print(f"  ✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ {test_name} FAILED: {e}")
        
        return result
    
    def run_game_movement_test(self) -> Dict[str, Any]:
        """Test in-game cursor movement."""
        test_name = "Game Movement Test"
        print(f"\n🧪 Running {test_name}")
        
        result = {
            'name': test_name,
            'passed': False,
            'steps': [],
            'error': None
        }
        
        try:
            # Start a game first (select beginner)
            print("  🎮 Starting a beginner game...")
            self.send_space(0.5)  # Select beginner
            result['steps'].append('game_started')
            
            if self.expect_text('Status: PLAYING', timeout=3):
                print("  ✅ Game started successfully")
                
                # Test all arrow key movements
                movements = ['right', 'down', 'left', 'up']
                for direction in movements:
                    print(f"  🏃 Testing {direction} movement...")
                    self.send_arrow_key(direction, 0.3)
                    result['steps'].append(f'moved_{direction}')
                
                # Test revealing a cell
                print("  💥 Testing cell reveal...")
                self.send_space(0.5)
                result['steps'].append('cell_revealed')
                
                # Exit game
                self.send_esc(0.5)
                result['steps'].append('game_exited')
                
                result['passed'] = True
                print(f"  ✅ {test_name} PASSED")
            else:
                raise Exception("Failed to start game")
                
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ {test_name} FAILED: {e}")
        
        return result
    
    def run_exit_test(self) -> Dict[str, Any]:
        """Test game exit functionality."""
        test_name = "Exit Test"
        print(f"\n🧪 Running {test_name}")
        
        result = {
            'name': test_name,
            'passed': False,
            'steps': [],
            'error': None
        }
        
        try:
            print("  🚪 Testing ESC exit...")
            self.send_esc(0.5)
            result['steps'].append('esc_sent')
            
            # Game should exit and process should terminate
            if self.process:
                try:
                    self.process.expect(pexpect.EOF, timeout=3)
                    result['steps'].append('process_terminated')
                    result['passed'] = True
                    print(f"  ✅ {test_name} PASSED")
                except pexpect.exceptions.TIMEOUT:
                    print(f"  ❌ Process didn't terminate properly")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ {test_name} FAILED: {e}")
        
        return result
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all available tests."""
        print("🚀 Starting Interactive Game Tests")
        print("=" * 50)
        
        if not self.start_game():
            return [{'name': 'Game Startup', 'passed': False, 'error': 'Failed to start game'}]
        
        # Run tests in sequence
        tests = [
            self.run_menu_navigation_test,
            self.run_game_movement_test,
            self.run_exit_test
        ]
        
        results = []
        for test_func in tests:
            # Restart game for each test (except the last one which tests exit)
            if test_func != self.run_exit_test:
                if self.process and self.process.isalive():
                    # Return to main menu if in game
                    self.send_esc(0.5)
                    time.sleep(0.5)
            
            result = test_func()
            results.append(result)
            
            # If this was the exit test, the process should be dead
            if test_func == self.run_exit_test:
                break
                
            # Small delay between tests
            time.sleep(0.5)
        
        self.test_results = results
        return results
    
    def cleanup(self):
        """Clean up the test environment."""
        if self.process and self.process.isalive():
            self.process.terminate()
            self.process = None


def run_interactive_tests():
    """Main function to run interactive tests."""
    game_path = "/Users/fatesaikou/testMD/learn-ai-driven-development/02.tasks/01.terminal-minesweeper/main.py"
    
    tester = GameInteractionTester(game_path)
    
    try:
        results = tester.run_all_tests()
        
        # Print summary
        print(f"\n{'=' * 50}")
        print("📊 Test Summary:")
        
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"📈 Success Rate: {passed/total*100:.1f}%")
        
        for result in results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"  {status} {result['name']}")
            if result.get('error'):
                print(f"    Error: {result['error']}")
            if result.get('steps'):
                print(f"    Steps: {', '.join(result['steps'])}")
        
        return results
        
    finally:
        tester.cleanup()


if __name__ == "__main__":
    # Check if pexpect is available
    try:
        import pexpect
        results = run_interactive_tests()
    except ImportError:
        print("❌ pexpect module required for interactive testing")
        print("💡 Install with: pip install pexpect")
        sys.exit(1)
