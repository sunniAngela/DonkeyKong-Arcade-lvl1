# DonkeyKong-Arcade-lvl1
This project is a recreation of the classic Donkey Kong Arcade game in Python. It was developed as the final project for the Programming course during my first year at university, so please bear with the bugs. The game features a simplified version of the first level of the original game.

## Installation

To run the game, you need to install the `pyxel` library using the following command.

**Windows**

```sh
pip install -U pyxel
```

**Linux**

```sh
sudo pip3 install -U pyxel
```

## How to Play

- Use the arrow keys (<kbd>↑</kbd>, <kbd>→</kbd>, <kbd>↓</kbd>, <kbd>←</kbd>) to control Mario's movement.
- Press <kbd>Space</kbd> to jump.
- The objective of the game is to reach Pauline in order to save her while avoiding the barrels.
- When you touch a barrel, you lose a life. The game ends when Mario loses all 3 lives.

## Files and Directory Structure

The project directory is organized as follows:
- **src/**: Contains the source code files
    - **main.py**: The main Python file that runs the game.
    - **game_elements/**: A subdirectory containing the class files for the different game elements.
        - **barrel.py**: Contains the class definition for the barrels in the game.
        - **constants.py**: Contains game constants such as window width and height and object positions.
        - **ladder.py**: Contains the class definition for the ladders in the game.
        - **mario.py**: Contains the class definition for the main character in the game, Mario.
        - **onboard.py**: Contains the definition for the superclass that all inanimate objects represented in the game inherit from.
        - **platforms.py**: Contains the class definition for the platforms in the game.
- **assets/**: A subdirectory containing the class files for the different game elements.
    - **sprites.pyxres**: Sprite definitions used in the game.
    - **sprites2.pyxres**: Additional sprites (not used in the game).
    - **sprites3.pyxres**: Additional sprites (not used in the game).