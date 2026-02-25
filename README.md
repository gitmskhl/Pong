# Pong (Pygame)
Classic Pong game implementation built with Python and Pygame.  
The project includes a playable single-player mode against AI with multiple difficulty levels and an in-game menu.

![example](media/pong.gif)

## Features
- Classic Pong gameplay loop.
- AI opponent with configurable difficulty.
- Pause/menu system with settings.
- Sound effects and score tracking.

## Tech Stack
- Python 3
- Pygame

## Requirements
- Python 3.10+ (recommended)
- `pip`

## Installation and Run
### Linux (Debian/Ubuntu)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pong.py
```

### Windows (PowerShell)
```powershell
python3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python3 pong.py
```

## Controls
- `Up Arrow` / `Down Arrow`: move left paddle
- `Space`: toggle AI control for left paddle (when AI mode is enabled)
- `Esc`: open/close pause menu

## Project Structure
- `pong.py` - game loop and core gameplay logic
- `menu.py` - menus and settings UI
- `config.py` - constants and runtime configuration
- `audio/` - sound assets
- `media/` - media assets (including the demo GIF)

## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.
