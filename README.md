# Alpha Chess Engine

Alpha is a lightweight Python chess engine built on python-chess, focused on material evaluation, tactical gains, and basic positional ideas.
It uses a selective search approach instead of full minimax, making it faster and easier to experiment with.

Status: `Early Beta (0.1.0b)`

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
