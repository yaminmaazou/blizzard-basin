
from collections import deque
from state import State
from solver import Solver
from world import World


class BFS(Solver):
    def __init__(self,
                world: World,
                initial_state: State) -> None:
        self.world = world
        self.initial_state = initial_state
        self.queue: deque[State] = deque([initial_state])
        self.visited: set[State] = set()
        self.visited.add(initial_state)
        self.current_time: int = initial_state.time
    
    # returns the final state if a solution is found, otherwise None
    def solve(self, forward: bool = True) -> State | None:
        while self.queue:
            current_state = self.queue.popleft()
            if current_state.time > self.current_time:
                self.world.step()
                self.current_time = current_state.time
                self.visited.clear()
            if self.world.is_dead(current_state.player_x, current_state.player_y):
                continue
            if self.world.is_solved(current_state.player_x, current_state.player_y, forward):
                return current_state
            for move in self.world.legal_moves(current_state.player_x, current_state.player_y):
                next_state = current_state.next(move)
                if next_state in self.visited:
                    continue
                self.visited.add(next_state)
                self.queue.append(next_state)
        return None