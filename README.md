# MonkFish Chess Engine 🐟
*The Zen of Chess* 🧘‍♂️    **[🔗 Live Demo](https://imraghavojha.github.io/monkfish-link/)**


<img src="TestGames/g0.gif" width="400">

## Quick Start ⚡
```bash
# One command setup - downloads everything automatically
python3 setup.py
```
Then add MonkFish to your chess GUI using `MonkFish.sh` as the engine command. See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## Description
MonkFish is a chess engine that maintains perfect balance, only capitalizing on its opponent's missteps. Like a Zen master, it doesn't force advantages but rather lets players create their own downfall. Built on Stockfish's powerful evaluation, MonkFish chooses moves that maintain equality, making it a mirror that reflects your own chess journey. Every loss against MonkFish is a lesson in self-inflicted defeat. ♟️

## Philosophy 🎯
- *"Every move a meditation"*
- *"Victory through self-defeat"*
- *"The stillness before the fall"*

## Technical Details ⚙️
A modified Stockfish engine that seeks positions with minimal advantage, playing the most equal continuation until the opponent creates winning chances through their own moves. Uses deep calculation and multiple principal variations to find the most balanced positions possible.
see [Technical Overview](/TECHNICAL_OVERVIEW.md)

## Reviews 💭
> "I was winning... I think I was winning... was I winning? No, I defeated myself."
> - Raghav, 1300 Rated Player

> "Played against it for 2 hours. Lost every game. Reviewed them all. It was just waiting... menacingly... before I blundered. Every. Single. Time."
> - Magnus Carlsend, Definitely Not The Real Magnus

> "The most passive-aggressive chess engine I've ever played."
> - Weak Stockfish, Chess Engine

> "Me: makes brilliant move
> MonkFish: I am one with the position
> Me: blunders queen
> MonkFish: The student becomes the teacher"
> - Martin, Chess.com

## Installation 🛠️

### Easy Way (Recommended)
```bash
python3 setup.py
```
The setup script automatically:
- Downloads the correct Stockfish binary for your system  
- Sets up all permissions
- Creates default configuration
- Tests that everything works

### Manual Way
If you prefer the old method:
1. Prerequisites:
    - Python 3.6+
    - A UCI-compatible chess GUI
    - Download stockfish binary from [Official Stockfish Repository](https://github.com/official-stockfish/Stockfish/releases)

2. Setup:
    ```bash
    # Make files executable
    chmod +x stockfish
    chmod +x MonkFish.sh
    ```

## Usage 🎮

### With Chess GUIs (Recommended):
1. **Cute Chess**: Engines → Configure Engines → Add
2. **Arena Chess**: Engines → Install New Engine  
3. **Any UCI GUI**: Add engine with these settings:
   - **Command**: `/full/path/to/MonkFish.sh`
   - **Working Directory**: `/full/path/to/MonkFish/folder`
   - **Protocol**: UCI

### Command Line Testing:
```bash
python3 uci.py
# Then type: uci, position startpos moves e2e4, go depth 2, quit
```

## Configuration ⚙️
Edit `monkfish_config.json` to customize MonkFish's zen level:
```json
{
  "engine": {
    "skill_level": 3,          // 0-20 (higher = stronger)
    "drawing_threshold": 0.01  // Lower = more zen
  }
}
```

## Files 📁
- `monkfish.py` - Core engine logic
- `uci.py` - UCI interface  
- `config.py` - Configuration system
- `uci_options.py` - UCI options handling
- `MonkFish.sh` - Shell script for GUI integration
- `setup.py` - Automatic setup script
- `tests/` - Test suite
- `stockfish` - Downloaded automatically by setup

## Troubleshooting 🔧
- **"Stockfish not found"**: Run `python3 setup.py`
- **"Permission denied"**: Run `chmod +x MonkFish.sh stockfish`
- **Engine too strong/weak**: Edit `skill_level` in `monkfish_config.json`
- **Need help**: Check [QUICKSTART.md](QUICKSTART.md)

## Credits 🙏
Built on Stockfish, modified to achieve enlightenment through equality.

*Note: Your defeat was within you all along.* 🪞
