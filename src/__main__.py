from solver import Solver
from bfs import BFS
from graphics import Graphics
from state import State
from parser import parse
from world import World

import argparse
from collections import deque


def choose_solver(algorithm: str, world: World, state0: State) -> Solver:
    match algorithm:
        case "bfs":
            return BFS(world, state0)
        case _:
            print("Error: Invalid algorithm identifier.")
            quit()


def main(file_path: str,
        manual: bool,
        algorithm: str,
        part1_only: bool,
        no_gui: bool,
        quiet: bool) -> None:
    try:
        with open(file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    map_int: list[list[int]]
    entry_x: int
    exit_x: int
    map_int, entry_x, exit_x = parse(content)

    world: World = World(map_int, entry_x, exit_x)
    state0: State = State(
        player_x = entry_x,
        player_y = -1,
        time = 0,
    )

    graphics: Graphics

    if manual:
        graphics = Graphics(world)
        graphics.run_manual()
        quit()

    phase_1_solver: Solver = choose_solver(algorithm, world, state0)
    phase_1_state: State | None = phase_1_solver.solve(forward=True)
    final_state: State | None = None

    if part1_only:
        final_state = phase_1_state
    else:
        # phase 2
        if phase_1_state is not None:
            phase_2_solver: Solver = choose_solver(algorithm, world, phase_1_state)
            phase_2_state: State | None = phase_2_solver.solve(forward=False)
            if phase_2_state is not None:
                # phase 3
                phase_3_solver: Solver = choose_solver(algorithm, world, phase_2_state)
                final_state = phase_3_solver.solve(forward=True)
            else:
                print("No solution found in phase 2.")
                quit()
        else:
            print("No solution found in phase 1.")
            quit()

    if final_state is None:
        print("No solution found.")
        quit()
    
    if quiet:
        print(f"{final_state.time}")
        quit()

    # walk back solution path
    current_state: State | None = final_state
    solution: deque[State] = deque([final_state])

    while current_state is not None:
        previous_state: State | None = current_state.previous
        if previous_state is not None:
            solution.appendleft(previous_state)
        current_state = previous_state

    fresh_world: World = World(map_int, entry_x, exit_x)  # fresh world for drawing, the original world is no longer at step 0
    # print solution path
    if no_gui:
        for state in solution:
            print(f"Step {state.time}:")
            print(fresh_world.draw(state.player_x, state.player_y))
            fresh_world.step()
        print (f"Total steps: {len(solution) - 1}") # initial state is not counted
    else:
        graphics = Graphics(fresh_world)
        graphics.run(solution)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description = "Solve AOC 2022 Day 24 (Blizzard Basin) for a given input. See the README file for more info.", usage="%(prog)s FILE_PATH [options]")
    
    argparser.add_argument("file", metavar="FILE_PATH", type = str, default = "", help = "Path to the input file")
    
    # flags
    argparser.add_argument("-m", "--manual", action = "store_true", help = "Control the simulation manually.")
    argparser.add_argument("-a", "--algorithm", type = str, default = "bfs", help = "Algorithm to use (bfs, ...). Not implemented.")
    argparser.add_argument("--part1", action = "store_true", help = "Only run part 1.")
    argparser.add_argument("--no-gui", action = "store_true", help = "Print solution to the console.")
    argparser.add_argument("-q", "--quiet", action = "store_true", help = "Only print the required number of steps to the console (implies --no-gui).")

    args = argparser.parse_args()

    file_path = args.file
    manual = args.manual
    algorithm = args.algorithm
    part1_only = args.part1
    no_gui = args.no_gui
    quiet = args.quiet

    main(file_path, manual, algorithm, part1_only, no_gui, quiet)