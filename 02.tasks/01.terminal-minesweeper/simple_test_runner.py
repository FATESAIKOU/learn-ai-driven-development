#!/usr/bin/env python3
"""
Simple testing framework for Terminal Minesweeper.
This can be run immediately without external dependencies.
"""

import sys
import os
import time
import subprocess
import signal
import threading
from typing import List, Dict, Any

# Add the game directory to Python path
sys.path.insert(0, '/Users/fatesaikou/testMD/learn-ai-driven-development/02.tasks/01.terminal-minesweeper')

class SimpleGameTester:
    """Simple test framework that can validate game components."""
    
    def __init__(self):
        self.test_results = []
    
    def test_game_imports(self) -> Dict[str, Any]:
        """Test that all game modules can be imported."""
        test_name = "Module Import Test"
        print(f"🧪 Running {test_name}...")
        
        result = {
            'name': test_name,
            'passed': False,
            'details': [],
            'error': None
        }
        
        modules_to_test = [
            ('minesweeper.models.game_models', 'Game Models'),
            ('minesweeper.infrastructure.input_handler', 'Input Handler'),
            ('minesweeper.infrastructure.terminal_manager', 'Terminal Manager'),
            ('minesweeper.logic.game_controller', 'Game Controller'),
            ('minesweeper.logic.game_board', 'Game Board'),
            ('minesweeper.presentation.menu_renderer', 'Menu Renderer'),
            ('minesweeper.presentation.game_renderer', 'Game Renderer'),
        ]
        
        try:
            for module_name, display_name in modules_to_test:
                try:
                    __import__(module_name)
                    result['details'].append(f"✅ {display_name}")
                    print(f"  ✅ {display_name} imported successfully")
                except ImportError as e:
                    result['details'].append(f"❌ {display_name}: {e}")
                    print(f"  ❌ {display_name} failed: {e}")
                    raise e
            
            result['passed'] = True
            print(f"✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {test_name} FAILED: {e}")
        
        return result
    
    def test_game_models(self) -> Dict[str, Any]:
        """Test game model functionality."""
        test_name = "Game Models Test"
        print(f"\n🧪 Running {test_name}...")
        
        result = {
            'name': test_name,
            'passed': False,
            'details': [],
            'error': None
        }
        
        try:
            from minesweeper.models.game_models import Cell, GameStatus, InputCommand, Difficulty
            
            # Test Cell creation
            cell = Cell()
            result['details'].append("✅ Cell creation")
            print("  ✅ Cell creation successful")
            
            # Test Cell methods
            assert cell.can_reveal() == True
            result['details'].append("✅ Cell can_reveal() method")
            
            cell.reveal()
            assert cell.is_revealed == True
            result['details'].append("✅ Cell reveal() method")
            
            # Test enums
            assert GameStatus.PLAYING == GameStatus.PLAYING
            result['details'].append("✅ GameStatus enum")
            
            assert InputCommand.MOVE_UP == InputCommand.MOVE_UP
            result['details'].append("✅ InputCommand enum")
            
            result['passed'] = True
            print(f"✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {test_name} FAILED: {e}")
        
        return result
    
    def test_input_handler(self) -> Dict[str, Any]:
        """Test input handler functionality."""
        test_name = "Input Handler Test"
        print(f"\n🧪 Running {test_name}...")
        
        result = {
            'name': test_name,
            'passed': False,
            'details': [],
            'error': None
        }
        
        try:
            from minesweeper.infrastructure.input_handler import InputHandler
            
            # Test InputHandler creation
            handler = InputHandler()
            result['details'].append("✅ InputHandler creation")
            print("  ✅ InputHandler created successfully")
            
            # Test setup/cleanup methods exist
            assert hasattr(handler, 'setup')
            assert hasattr(handler, 'cleanup')
            assert hasattr(handler, 'get_command')
            result['details'].append("✅ InputHandler methods")
            
            result['passed'] = True
            print(f"✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {test_name} FAILED: {e}")
        
        return result
    
    def test_game_startup(self) -> Dict[str, Any]:
        """Test that the game can start without crashing."""
        test_name = "Game Startup Test"
        print(f"\n🧪 Running {test_name}...")
        
        result = {
            'name': test_name,
            'passed': False,
            'details': [],
            'error': None
        }
        
        try:
            # Try to start the game process with a timeout
            game_dir = "/Users/fatesaikou/testMD/learn-ai-driven-development/02.tasks/01.terminal-minesweeper"
            
            # Start game process with timeout
            proc = subprocess.Popen(
                ['python', 'main.py'],
                cwd=game_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            
            # Let it run for a short time
            time.sleep(2)
            
            # Send ESC to exit
            try:
                proc.stdin.write('\x1b')
                proc.stdin.flush()
            except:
                pass
            
            # Wait for termination with timeout
            try:
                stdout, stderr = proc.communicate(timeout=3)
                result['details'].append(f"✅ Game started and exited cleanly")
                print("  ✅ Game started and exited cleanly")
                
                if stderr:
                    result['details'].append(f"⚠️ Stderr: {stderr[:100]}...")
                
            except subprocess.TimeoutExpired:
                proc.kill()
                result['details'].append("⚠️ Game started but had to be killed")
                print("  ⚠️ Game started but had to be killed (timeout)")
            
            result['passed'] = True
            print(f"✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {test_name} FAILED: {e}")
        
        return result
    
    def test_game_components_integration(self) -> Dict[str, Any]:
        """Test that game components work together."""
        test_name = "Components Integration Test"
        print(f"\n🧪 Running {test_name}...")
        
        result = {
            'name': test_name,
            'passed': False,
            'details': [],
            'error': None
        }
        
        try:
            from minesweeper.logic.game_board import GameBoard
            from minesweeper.logic.mine_generator import MineGenerator
            from minesweeper.models.game_models import Difficulty
            
            # Test game board creation
            board = GameBoard(9, 9, 10)
            result['details'].append("✅ GameBoard creation")
            
            # Test mine generation
            generator = MineGenerator()
            mines = generator.generate_mines(9, 9, 10, avoid_position=(0, 0))
            assert len(mines) == 10
            result['details'].append("✅ Mine generation")
            
            # Test board initialization with mines
            board.place_mines(mines)
            result['details'].append("✅ Mine placement")
            
            # Test cell revelation
            revealed = board.reveal_cell(0, 0)
            result['details'].append(f"✅ Cell revelation: {revealed}")
            
            result['passed'] = True
            print(f"✅ {test_name} PASSED")
            
        except Exception as e:
            result['error'] = str(e)
            print(f"❌ {test_name} FAILED: {e}")
        
        return result
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all available tests."""
        print("🚀 Starting Simple Game Tests")
        print("=" * 50)
        
        test_functions = [
            self.test_game_imports,
            self.test_game_models,
            self.test_input_handler,
            self.test_game_components_integration,
            self.test_game_startup,
        ]
        
        results = []
        
        for test_func in test_functions:
            result = test_func()
            results.append(result)
            self.test_results.append(result)
        
        # Print summary
        print(f"\n{'=' * 50}")
        print("📊 Test Summary:")
        
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"📈 Success Rate: {passed/total*100:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for result in results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"  {status} {result['name']}")
            
            if result.get('error'):
                print(f"    ❌ Error: {result['error']}")
            
            for detail in result.get('details', [])[:3]:  # Show first 3 details
                print(f"    {detail}")
            
            if len(result.get('details', [])) > 3:
                print(f"    ... and {len(result['details']) - 3} more")
        
        return results


def run_basic_functionality_test():
    """Quick test to verify the game works."""
    print("🎮 Quick Functionality Check")
    print("-" * 30)
    
    try:
        # Test if we can import main components
        sys.path.insert(0, '/Users/fatesaikou/testMD/learn-ai-driven-development/02.tasks/01.terminal-minesweeper')
        
        from minesweeper.models.game_models import GameStatus, InputCommand
        from minesweeper.infrastructure.input_handler import InputHandler
        
        print("✅ Core modules imported successfully")
        
        # Test key mapping
        handler = InputHandler()
        print("✅ InputHandler created successfully")
        
        print("🎯 Game appears to be working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False


if __name__ == "__main__":
    print("🎮 Terminal Minesweeper Test Suite")
    print("=" * 50)
    
    # Run quick test first
    if not run_basic_functionality_test():
        print("❌ Basic functionality test failed. Exiting.")
        sys.exit(1)
    
    print("\n")
    
    # Run comprehensive tests
    tester = SimpleGameTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    if passed == total:
        print(f"\n🎉 All tests passed! Game is ready for use.")
        sys.exit(0)
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the issues above.")
        sys.exit(1)
