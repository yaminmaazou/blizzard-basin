# Advent Of Code 2022, Day 24 (Blizzard Basin)
This program solves the Advent of Code 2022, Day 24 problem using Python. For a detailed explanation of the problem, please refer to the official [Advent of Code 2022, Day 24](https://adventofcode.com/2022/day/24) page.

## Installation
To run the program, you need to have Python installed on your machine.  
Next, navigate to the directory where the script is located and install the required packages. You can do this globally or in a virtual environment (recommended).
### Using a Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Globally
```bash
pip install -r requirements.txt
```

## Controls
In GUI mode, you can use the following keyboard controls:
- **X**: Save the current frame as an SVG image.
- **Enter**: Start or pause the simulation.
- **Space**: Advance one step when paused.
- **Arrow Keys**: Move the player manually (only in manual mode).
- **Escape**: Quit the program.

## Usage
Navigate to the project directory and run the script with the input file as an argument. The input file should follow the format specified in the problem description. Some example input files are provided in the `samples` directory.
```bash
python ./src <input_file>
```
By default, the script will use Pygame to visualize the solution and allow for user interaction. 
For more options, see the Options section below, or run
```bash
python ./src --help
```
to see all available options.
### Options
#### Use manual input
```bash
python ./src <input_file> --manual
```
Allows manual navigation of the player, using the arrow keys.  
This option is useful for debugging or understanding the movement of the blizzards and the player, but does not solve the problem automatically.  
Overrides all other options.

#### Print to Console without GUI
```bash
python ./src <input_file> --no-gui
```
Print the solution steps to the console without using Pygame.

#### Print the required number of steps and nothing else
```bash
python ./src <input_file> --quiet
```

#### Only solve the first part of the problem
```bash
python ./src <input_file> --part1
```

#### Use a different algorithm
```bash
python ./src <input_file> --algorithm <algorithm_name>
```
Use a different algorithm for solving the problem. The currently available algorithms are:
- `bfs` (default): Breadth-First Search