from dataclasses import dataclass, field

@dataclass(frozen=True)
class State:
    player_x: int = 0
    player_y: int = -1
    time: int = 0
    # compare=False to speed up hashing and equality checks
    previous: "State | None" = field(default=None, compare=False)

    # advance the state by one step
    def next(self, move_direction: str = "") -> "State":
        player_x = self.player_x
        player_y = self.player_y
        time = self.time + 1
        match move_direction:
            case "<":
                player_x -= 1
            case "v":
                player_y += 1
            case ">":
                player_x += 1
            case "^":
                player_y -= 1
            case _:
                pass
        return State(
            player_x=player_x,
            player_y=player_y,
            time=time,
            previous=self
        )
    
    # these methods should be auto-generated
    # since self.previous is not part of the hash, they should be equivalent
    # TODO: compare runtime with and without these methods

    # def __eq__(self, other: "State3") -> bool:
    #     if not isinstance(other, State3):
    #         return False
    #     return self.player_x == other.player_x and \
    #             self.player_y == other.player_y and \
    #             self.time == other.time
    
    # def __hash__(self) -> int:
    #     return hash((self.player_x, self.player_y, self.time))