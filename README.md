# Alpha Chess Engine

Alpha is a lightweight Python chess engine built on python-chess, focused on material evaluation, tactical gains, and basic positional ideas.
It uses a selective search approach instead of full minimax, making it faster and easier to experiment with.

Status: `Early Beta (0.2.0b)`

## Features

### Custom Evaluation Function

- Material balance

- Capture rewards

- Central pawn control

- Bishop mobility

- Simple tactical gain detection

### Selective Move Search

- Examines only the top N candidate moves

- Reduces branching factor for speed

### Configurable Depth & Lines

- Adjust search depth and number of candidate lines

## Running the Engine
**Requirements:**
- Python 3.8+
- `python-chess`

Install dependencies:
```bash
pip install python-chess
```
Run:
```bash
python alpha.py
```

## How to play
- Enter moves in SAN format
Example:
```mathematica
e4
Nf3
Qxe5
0-0
```
- Special Commands:
- `fen` - Outputs current FEN
- `quit` - Quits the game

## Example Output:
```yaml
ALPHA 0.1.0b is starting...
San moves are accepted.
Your Move: e4
Computer plays: e5
Computer thought for 1.501 seconds.
```

## Strength
This is a strength table that shows the statistics of this engine playing a game against `Chess.com 3200 Elo bot`.
> Note this is only one game, one, just one.

### Alpha v0.1.0
| Site | ELO | CENTIPAWN LOSS | Accuracy |
|--------|--------|------------|---------|
| Chess.com | 1250 ELO | ~95-115 | 66% |
| Lichess.org   | ~950ELO | 77 | ~74-78% |
