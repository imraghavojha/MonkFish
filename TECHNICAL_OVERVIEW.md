# MonkFish Technical Documentation

## Architecture and Implementation

MonkFish uses Stockfish's core strength but changes how moves are selected. While traditional chess engines always choose the most aggressive moves, MonkFish looks for moves that keep the position balanced. This creates a unique playing style that waits for opponents to make mistakes rather than forcing advantages.

## Core Technology

Stockfish analyzes chess positions by building a game tree - mapping out possible moves and responses. For each position, it evaluates thousands of possibilities per second. MonkFish reads this analysis in real-time and specifically looks for moves that lead to equal positions.

Instead of changing Stockfish's complex code, we built a system that reads its output and selects moves differently. This approach has major benefits:

- We keep Stockfish's powerful ability to analyze positions
- The code stays fast and efficient
- Updates to Stockfish don't break our modifications

## How Move Selection Works

MonkFish processes positions in several steps:

1. Analyzes positions 20 moves deep for accurate evaluation
2. Considers 25 different possible moves at each position
3. Looks for moves that lead to near-equal positions (within ±0.01)
4. Uses classical chess understanding rather than neural network tactics

This creates an engine that maintains balanced positions while avoiding forced tactical sequences.

## Performance Settings

The engine achieves its balanced style through carefully chosen parameters:

- Depth of 20 moves provides strong but not overwhelming analysis
- Skill Level 4 introduces some controlled variation in play
- MultiPV 25 ensures we examine enough move choices
- Disabled neural network reduces aggressive tactical calculations

## Adjusting Engine Strength

You can modify these key settings for different playing styles:

### Stronger Configuration:

```
Skill Level: 15-20
Analysis Depth: 25+ moves
Move Choices (MultiPV): 30+
Equality Threshold: ±0.005
```

### Weaker Configuration:

```
Skill Level: 1-5
Analysis Depth: 15-18 moves
Move Choices (MultiPV): 15-20
Equality Threshold: ±0.01
```

## Technical Benefits

Our approach offers clear advantages:

- Uses Stockfish's efficient position analysis
- Maintains high performance
- Code remains easy to update
- Simple to modify and adjust settings
