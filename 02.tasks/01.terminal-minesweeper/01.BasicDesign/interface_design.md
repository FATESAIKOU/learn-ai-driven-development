# Interface Design - Terminal Minesweeper

## User Interface Specifications

### 1. Main Menu Interface

```
╔══════════════════════════════════════╗
║           TERMINAL MINESWEEPER       ║
╠══════════════════════════════════════╣
║                                      ║
║  > Beginner    (9x9, 10 mines)      ║
║    Intermediate (16x16, 40 mines)    ║
║    Expert      (30x16, 99 mines)     ║
║    Custom      (User defined)        ║
║    Exit                              ║
║                                      ║
║  Use ↑↓ to navigate, SPACE to select ║
║  ESC to exit                         ║
╚══════════════════════════════════════╝
```

### 2. Game Interface Layout

```
╔══════════════════════════════════════════════════════════╗
║  Time: 045  |  Mines: 008  |  Status: PLAYING           ║
╠══════════════════════════════════════════════════════════╣
║    A B C D E F G H I                                     ║
║  1 █ █ █ █ █ █ █ █ █                                     ║
║  2 █ █ █ 1 2 2 1 █ █                                     ║
║  3 █ █ █ █ █ █ █ █ █                                     ║
║  4 █ █ █ █ █ █ █ █ █                                     ║
║  5 █ █ █ ▓ █ █ █ █ █  ← Cursor position                  ║
║  6 █ █ █ █ █ █ █ █ █                                     ║
║  7 █ F █ █ █ █ █ █ █                                     ║
║  8 █ █ █ █ █ █ █ █ █                                     ║
║  9 █ █ █ █ █ █ █ █ █                                     ║
║                                                          ║
║  Controls: ↑↓←→ Move | SPACE Reveal | Q Flag | ESC Exit  ║
╚══════════════════════════════════════════════════════════╝
```

### 3. Game Over Interface

#### Win Screen
```
╔══════════════════════════════════════╗
║              YOU WIN!                ║
╠══════════════════════════════════════╣
║                                      ║
║  Time: 02:34                         ║
║  All mines found!                    ║
║                                      ║
║  > Play Again                        ║
║    Main Menu                         ║
║    Exit                              ║
║                                      ║
║  Use ↑↓ to navigate, SPACE to select ║
╚══════════════════════════════════════╝
```

#### Loss Screen
```
╔══════════════════════════════════════╗
║             GAME OVER                ║
╠══════════════════════════════════════╣
║                                      ║
║  You hit a mine!                     ║
║  Time: 01:23                         ║
║                                      ║
║  > Play Again                        ║
║    Main Menu                         ║
║    Exit                              ║
║                                      ║
║  Use ↑↓ to navigate, SPACE to select ║
╚══════════════════════════════════════╝
```

## Character Set Definitions

### Cell Display Characters
- **Hidden Cell**: `█` (Full block)
- **Cursor on Hidden**: `▓` (Dark shade block) 
- **Revealed Empty**: ` ` (Space)
- **Revealed Numbers**: `1` `2` `3` `4` `5` `6` `7` `8`
- **Flagged Cell**: `F`
- **Mine (Game Over)**: `*`
- **Wrong Flag (Game Over)**: `X`

### Border Characters
- **Horizontal**: `═`
- **Vertical**: `║`
- **Top Left**: `╔`
- **Top Right**: `╗`
- **Bottom Left**: `╚`
- **Bottom Right**: `╝`
- **T-Junction Down**: `╦`
- **T-Junction Up**: `╩`
- **T-Junction Right**: `╠`
- **T-Junction Left**: `╣`

### Color Scheme (ANSI Colors)
- **Background**: Default terminal background
- **Border**: Bright White
- **Numbers**: 
  - 1: Blue
  - 2: Green  
  - 3: Red
  - 4: Purple
  - 5: Maroon
  - 6: Turquoise
  - 7: Black
  - 8: Gray
- **Cursor**: Inverse/Highlighted
- **Flag**: Yellow
- **Mine**: Red
- **Status Bar**: Cyan

## Input Command Mapping

### Keyboard Input to Commands
```python
INPUT_MAPPING = {
    # Navigation
    '\x1b[A': 'MOVE_UP',      # Up arrow
    '\x1b[B': 'MOVE_DOWN',    # Down arrow  
    '\x1b[C': 'MOVE_RIGHT',   # Right arrow
    '\x1b[D': 'MOVE_LEFT',    # Left arrow
    
    # Actions
    ' ': 'SELECT',            # Space
    'q': 'FLAG',              # Q key
    'Q': 'FLAG',              # Q key (uppercase)
    '\x1b': 'EXIT',           # ESC key
    '\x03': 'FORCE_EXIT',     # Ctrl+C
}
```

### Menu Navigation
- **Arrow Keys**: Navigate menu options
- **Space**: Select highlighted option
- **ESC**: Exit application

### Game Navigation  
- **Arrow Keys**: Move cursor on board
- **Space**: Reveal cell at cursor position
- **Q**: Toggle flag at cursor position
- **ESC**: Return to main menu (with confirmation)

## Display Refresh Strategy

### Partial Rendering
- Only redraw changed areas to minimize flicker
- Use cursor positioning to update specific cells
- Full refresh only on game state changes

### Buffer Management
- Maintain screen buffer for efficient updates
- Track dirty regions for selective rendering
- Clear screen only when necessary

## Responsive Design Considerations

### Terminal Size Adaptation
- Minimum terminal size: 80x24 characters
- Center game board if terminal is larger
- Provide warning if terminal is too small
- Graceful degradation for smaller screens

### Performance Optimization
- Efficient screen update algorithms
- Minimal ANSI escape sequence usage
- Optimized redraw cycles for smooth gameplay
