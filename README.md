
# Tile Flip-Memory Game

## Overview

This is a tile-flip memory game built using Python and Pygame. The game challenges players to match pairs of images by flipping tiles. The game keeps track of player scores and stores them in an SQLite database.

## Features

- Memory game with tiles to flip and match.
- Stores player names and scores in an SQLite database.
- Displays top 5 players and their times.
- Simple user interface with Pygame.

## Requirements

- Python 3.x
- Pygame
- SQLite3

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tile-flip-memory-game.git
   cd tile-flip-memory-game
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

3. Ensure you have a folder named `images` in the project directory with your image files for the game. Example image filenames should be in the format `imagename.png`.

## How to Play

1. Run the game:
   ```bash
   python app.py
   ```

2. Enter your name in the input box and press Enter.

3. Click on the tiles to flip them and try to match pairs of images.

4. The game tracks the time taken to match all pairs. Your score will be recorded in the database.

5. View the top 5 players and their times on the screen.

6. After completing the game, you can choose to restart or quit by pressing 'R' or 'Q'.

## Code Structure

- `app.py`: Main application file containing the game logic and Pygame loop.
- `images/`: Directory containing image files used in the game.
- `game_data.db`: SQLite database file to store player names and scores.

## Database Structure

- `Players`: Table to store player information.
  - `id`: Primary key.
  - `player_name`: Name of the player.

- `Scores`: Table to store game scores.
  - `id`: Primary key.
  - `player_id`: Foreign key referencing the `Players` table.
  - `time_taken`: Time taken by the player to complete the game.

## Future Enhancements

- Add more levels with increasing difficulty.
- Implement a better UI/UX design.
- Add sound effects and background music.
- Allow players to select different image sets.

## Acknowledgments

- Pygame library for game development.
- SQLite3 for database management.
