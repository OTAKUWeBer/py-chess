# Chess Game

This is a simple chess game built with Python using the `pygame` and `python-chess` libraries. It features a graphical chessboard, valid move highlighting, and basic game rules including check, checkmate, and stalemate detection. You can play in **Two-Player** mode or **Bot vs Player** mode where the bot is powered by the Stockfish engine.

## Features

- **Graphical Chessboard**: Interactive chessboard rendered using `pygame`.
- **Valid Move Highlighting**: Highlights all valid moves for the selected piece.
- **Check and Checkmate Indicators**: Displays visual indicators for check and checkmate scenarios.
- **Win or Draw Messages**: Displays the winner or a draw message when the game ends.
- **Fully Playable**: Supports all standard chess rules for two players or player vs bot.

## Prerequisites

To run this project, you need:

- Python 3.7 or higher
- `pygame` library
- `python-chess` library
- **Stockfish Engine** (for bot gameplay)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/OTAKUWeBer/py-chess.git
cd py-chess
```

### 2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Install Stockfish

**For Linux (Debian-based, Ubuntu, etc.)**:

```bash
sudo apt-get update
sudo apt-get install stockfish
```

**For macOS (via Homebrew)**:

```bash
brew install stockfish
```

**For Windows**:

1. Download the latest Stockfish release from [the official Stockfish website](https://stockfishchess.org/download/).
2. Extract the downloaded ZIP file.
3. Note the directory where you extracted Stockfish. For example, `C:\Stockfish`.

**For all platforms**: Make sure the Stockfish executable is available in the system's `PATH`, or update the `main.py` file to point to the Stockfish binary location.

For example, change the line in the code where Stockfish is initialized:

```python
engine = chess.engine.SimpleEngine.popen_uci("/path/to/stockfish")
```

Replace `"/path/to/stockfish"` with the correct path to the Stockfish executable.

### 4. Make sure to have the chess piece images in the `assets/pieces` directory:

- `white-pawn.png`, `white-rook.png`, `white-knight.png`, `white-bishop.png`, `white-queen.png`, `white-king.png`
- `black-pawn.png`, `black-rook.png`, `black-knight.png`, `black-bishop.png`, `black-queen.png`, `black-king.png`

## Usage

1. Run the game:
   ```bash
   python main.py
   ```

2. Play chess! Use the mouse to select and move pieces.

3. Press `Esc` to quit the game.

## How to Play

1. The game starts with the white player's turn.
2. Click on a piece to view its valid moves (highlighted with green dots).
3. Click on a valid destination square to move the selected piece.
4. The game detects check, checkmate, and stalemate scenarios.
5. You can choose between:
   - **Two-Player Mode**: Both players take turns on the same device.
   - **Bot vs Player Mode**: Play against the Stockfish-powered bot, with the human player going first.

## Game Controls

- **Left Mouse Click**: Select a piece and make moves.
- **Esc**: Quit the game.

## Contributing

Contributions are welcome! Feel free to submit a pull request or create an issue if you find any bugs or have feature suggestions.