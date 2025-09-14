from abc import ABC, abstractmethod
from state import State

class Solver(ABC):
    # returns the final state if a solution is found, otherwise None
    @abstractmethod
    def solve(self, forward: bool) -> State | None:
        return None