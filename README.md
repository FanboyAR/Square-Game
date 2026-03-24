# Square Game

Square Game is a progression-based maze runner built with pygame-ce. You guide a square through generated mazes, collect coins, buy upgrades, unlock skins, and keep advancing levels with persistent save data.

## Features

- Randomly generated mazes that scale with level progression
- Smooth movement with wall collision and coin collection
- Store upgrades for speed, coin bonus, and prestige power
- Prestige/reset system with reward preview before reset
- Customization menu with unlockable skins:
   - Free/default skins
   - Coin-purchasable skins
   - Level-unlock skins
   - Prestige skins
- Gradient skin variants (including patterned gradients)
- Full RGB sliders for selected skin color customization
- Display settings menu:
   - Windowed / Fullscreen / Borderless modes
   - Resolution selection + Auto resolution mode
- Persistent progress and settings saves

## Requirements

- Python 3.11+
- `pygame-ce`

## Installation

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd Square_Game
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Run

```bash
python "square game.py"
```

## Controls

- **WASD / Arrow Keys**: Move player
- **Mouse**: Navigate menus and click buttons
- **Enter / Space**: Start game from main menu
- **ESC**:
   - In gameplay: open/return via pause flow
   - In menus: go back (where applicable)
- **F11**: Quick toggle between windowed and fullscreen

## Save Files

- `progress.json`: level, coins, upgrades, prestige, unlocked/selected skins, custom skin RGB
- `mid_save.json`: in-level checkpoint/state data
- `settings.json`: display mode and resolution preferences

## Notes

- The game window title is **Square Game**.
- Auto resolution adapts to selected window mode.
- If pygame is missing, install with:
   ```bash
   pip install pygame-ce
   ```