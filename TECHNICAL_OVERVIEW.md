# MonkFish Technical Documentation

## Overview

MonkFish is a chess engine built on Stockfish that focuses on balanced, positional play rather than aggressive tactics. While most chess engines constantly seek advantages, MonkFish aims to maintain equality and capitalize on opponent mistakes.

## How It Works

## Understanding Stockfish Architecture
Stockfish, the foundation of MonkFish, is a sophisticated chess engine that combines several key components:
Search Algorithm
Stockfish uses an advanced alpha-beta search algorithm to analyze chess positions:

Move Generation

Generates all legal moves in a position
Uses bitboards (64-bit integers) to represent the chess board
Efficiently tracks piece positions and possible moves


Position Evaluation

Evaluates positions using both material and positional factors
Considers piece placement, king safety, pawn structure
Uses a sophisticated evaluation function tuned through machine learning


Tree Search

Examines millions of positions per second
Uses alpha-beta pruning to eliminate unpromising variations
Implements advanced search techniques:

Null move pruning
Late move reduction
Futility pruning
Transposition tables

### Basic Architecture

MonkFish doesn't modify Stockfish's core code. Instead, it creates a wrapper that:
1. Reads Stockfish's position analysis tree in real time
2. Applies custom move selection algorithm
3. Chooses moves that maintain balanced positions

This approach preserves Stockfish's powerful analysis capabilities while implementing a different playing philosophy.

### Move Selection Process

When choosing a move, MonkFish:
1. Analyzes positions up to 20 moves ahead
2. Evaluates 25 candidate moves per position
3. Prioritizes moves leading to equal positions (within ±0.01)
4. Relies on traditional chess principles rather than neural network analysis

The result is an engine that plays solid, positional chess instead of forcing tactical complications.

### Key Technical Features

- Reads and processes Stockfish output in real-time
- Maintains high computational efficiency
- Updates smoothly when new Stockfish versions release
- Preserves all core analysis capabilities

## Configuration Guide

### Standard Settings

- Analysis Depth: 20 moves
- Skill Level: 4
- Move Candidates (MultiPV): 25
- Neural Network: Disabled

These settings create MonkFish's characteristic balanced style.

### Customization Options

You can adjust MonkFish's strength using these parameters:

For Stronger Play:
```
Skill Level: 15-20
Analysis Depth: 25+ moves
Move Candidates: 30+
Position Equality Range: ±0.005
```

For Casual Play:
```
Skill Level: 1-5
Analysis Depth: 15-18 moves
Move Candidates: 15-20
Position Equality Range: ±0.01
```

## Technical Advantages

1. Efficient Resource Usage
   - Leverages Stockfish's optimized position analysis
   - Maintains fast computation speed
   - Minimal memory overhead

2. Maintainable Design
   - Clean separation from Stockfish core
   - Easy to update when Stockfish releases new versions
   - Simple parameter adjustments for different playing styles

3. Reliable Performance
   - Stable evaluation criteria
   - Consistent playing strength
   - Predictable resource usage
