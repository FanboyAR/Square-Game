# Square Game

A simple Pygame application where you can move a square around the screen using arrow keys. The square is bounded within the screen edges.

## Requirements

- Python 3.11 or later
- pygame-ce

## Installation

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd square-game
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

Use arrow keys to move the square. Close the window to exit.

## Troubleshooting

- If you get "No module named 'pygame'", ensure pygame-ce is installed: `pip install pygame-ce`
- The game requires a display; it won't run in headless environments.