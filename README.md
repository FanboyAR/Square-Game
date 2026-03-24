# Square Maze Game

A maze-solving game where you control a square through randomly generated mazes. Navigate through walls to reach the goal and progress through increasingly challenging levels. Your progress is automatically saved.

## Features

- Main menu with start and quit options
- Randomly generated mazes for each level
- Collision detection with walls
- Progress saving (resumes from last completed level)
- Simple controls: arrow keys to move, ESC to return to menu

## Requirements

- Python 3.11 or later
- pygame-ce

## Installation

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd square-maze-game
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

Run the game with:
```
python "square game.py"
```

- Use mouse to click "Start Game" from the main menu
- Use arrow keys to move the red square through the maze
- Reach the green goal square to advance to the next level
- Press ESC during gameplay to return to the main menu
- Progress is automatically saved when you complete a level or quit

## Controls

- **Arrow Keys**: Move the square
- **ESC**: Return to main menu (saves progress)
- **Mouse**: Click buttons in menu

## Troubleshooting

- If you get "No module named 'pygame'", ensure pygame-ce is installed: `pip install pygame-ce`
- The game requires a display; it won't run in headless environments.
- Progress is saved in `progress.json` in the game directory