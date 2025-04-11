# Minesweeper with AI

This project implements the classic Minesweeper game with an AI assistant that can make intelligent moves based on logical inference. The game is built with Python and uses PyGame for the graphical interface.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Game Logic](#game-logic)
- [AI Algorithm](#ai-algorithm)
- [Implementation Details](#implementation-details)
- [Run The Game](#run-the-game)
- [How to Play](#how-to-play)

## Overview

Minesweeper is a single-player puzzle game where the objective is to clear a rectangular board containing hidden mines without detonating any of them. The player uses clues about the number of neighboring mines in each field to determine where the mines are.

This implementation includes a graphical interface and an AI assistant that can make intelligent moves based on logical deduction. You can see the knowledge building and in the console output as the AI makes a move.

## Project Structure

The project consists of two main Python files:

1. `minesweeper.py` - Contains the core game logic and AI implementation:

   - `Minesweeper` class - Manages the game state and rules
   - `Sentence` class - Represents logical statements for the AI
   - `MinesweeperAI` class - Implements the AI logic using knowledge-based approach

2. `runner.py` - Handles the game's graphical interface using Pygame:
   - Manages user input
   - Renders the game board
   - Coordinates between the game logic and AI

## Game Logic

The game follows standard Minesweeper rules with a slight modification: diagonal cells are not considered neighbors.

### Key Components

- **Game Board**: An 8x8 grid with 8 mines randomly placed
- **Cell States**:
  - Hidden (default)
  - Revealed (showing the number of adjacent mines)
  - Flagged (marked by the player as a potential mine)
- **Game End Conditions**:
  - Win: All mines are correctly flagged
  - Lose: A mine is revealed

## AI Algorithm

The AI uses a knowledge-based approach with propositional logic to make safe moves whenever possible.

### Knowledge Representation

The AI's knowledge is represented as a collection of sentences, where each sentence consists of:

- A set of cells
- A count of how many mines are in those cells

### Inference Process

1. **Basic Knowledge**: When a cell is revealed, the AI creates a sentence about its neighboring cells
2. **Inference Rules**:
   - If count = 0, all cells in the set are safe
   - If count = size of the set, all cells in the set are mines
   - If set1 ⊆ set2, then (set2 - set1) = (count2 - count1)

### Decision Making

1. **Safe Move**: Choose a cell known to be safe
2. **Random Move**: If no safe move is available, make a random move among cells not known to be mines

## Implementation Details

### Minesweeper Class

The `Minesweeper` class handles the game logic:

- **Initialization**: Sets up the board with randomly placed mines
- **Cell Evaluation**: Determines if a cell is a mine
- **Neighboring Mines**: Calculates how many mines are adjacent to a cell
- **Win Condition**: Checks if all mines have been correctly flagged

### Sentence Class

The `Sentence` class represents logical statements for the AI:

- **Structure**: A set of cells and a count of mines within those cells
- **Inference**: Methods to determine known mines and safe cells
- **Updates**: Methods to update knowledge when cells are marked as mines or safe

### MinesweeperAI Class

The `MinesweeperAI` class implements the AI's decision-making process:

- **Knowledge Base**: Maintains a list of sentences
- **Knowledge Updates**: Adds new information when a cell is revealed
- **Inference Engine**: Applies logical deduction to identify safe cells and mines
- **Decision Making**: Methods to make safe moves or random moves

#### Key AI Methods

1. `add_knowledge(cell, count)`: Updates the AI's knowledge when a cell is revealed
2. `mark_safe(cell)`: Marks a cell as safe and updates all knowledge accordingly
3. `mark_mine(cell)`: Marks a cell as a mine and updates all knowledge accordingly
4. `make_safe_move()`: Returns a known safe move if available
5. `make_random_move()`: Returns a random move if no safe move is available

### Knowledge Inference Example

If we have two sentences:

- {A, B, C} = 1
- {A, B} = 1

We can infer:

- {C} = (1 - 1) = 0, meaning C is safe

---

This implementation demonstrates how propositional logic can be used to create an AI that plays Minesweeper intelligently, making safe moves whenever possible based on logical deduction.

## Run the Game

- Install the requirements with `pip install -r requirements.txt`
- Run the game with `python runner.py`

## How to Play

1. **Start the Game**: Run `python runner.py` to launch the game
2. **Controls**:
   - Left-click a cell to reveal it
   - Right-click a cell to flag/unflag it as a mine
   - Click "AI Move" to let the AI make a move 9
   - Click "Reset" to start a new game
3. **Objective**: Mark all mines with flags without revealing any mines
