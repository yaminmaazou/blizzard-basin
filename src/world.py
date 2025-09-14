class World:
    def __init__(self,
                map: list[list[int]] = [[0]],
                entry_x: int = 0,
                exit_x: int = 0,) -> None:
        if not self._validate_map(map):
            raise ValueError("Invalid map format")
        if entry_x < 0 or entry_x >= len(map[0]):
            raise ValueError("entry_x must be within the map width")
        if exit_x < 0 or exit_x >= len(map[0]):
            raise ValueError("exit_y must be within the map height")

        self.width = len(map[0])
        self.height = len(map)
        self.map = map
        self.entry_x = entry_x
        self.exit_x = exit_x

    def _validate_map(self, map: list[list[int]]) -> bool:
        if not isinstance(map, list):
            return False
        if not isinstance(map[0], list):
            return False

        width: int = len(map[0])
        for row in map:
            if not isinstance(row, list):
                return False
            if len(row) != width:
                return False
            for cell in row:
                if cell >= 16 or cell < 0:
                    return False
        return True
    
    # player is standing in a blizzard
    def is_dead(self, player_x: int, player_y:int) -> bool:
        if player_y != -1 and player_y != self.height and self.map[player_y][player_x] != 0:
            return True
        return False
    
    # player is at the exit (i.e. beyond the last row)
    def is_solved(self, player_x: int, player_y: int, forward: bool = True) -> bool:
        if forward:
            if player_x == self.exit_x and player_y == self.height:
                return True
        else:
            if player_x == self.entry_x and player_y == -1:
                return True
        return False
    
    # move all blizzards
    def step(self) -> None:
        new_map: list[list[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]

        for i in range(self.width):
            for j in range(self.height):
                if self.map[j][i] & 1:  # '<'
                    new_map[j][self.width - 1 if i == 0 else i - 1] |= 1
                if self.map[j][i] & 2:  # 'v'
                    new_map[0 if j == self.height - 1 else j + 1][i] |= 2
                if self.map[j][i] & 4:  # '>'
                    new_map[j][0 if i == self.width - 1 else i + 1] |= 4
                if self.map[j][i] & 8:  # '^'
                    new_map[self.height - 1 if j == 0 else j - 1][i] |= 8
        
        self.map = new_map
    
    # return all possible moves the player can make
    def legal_moves(self, player_x: int, player_y: int) -> list[str]:
        moves: list[str] = []

        for move in ["", "<", "v", ">", "^"]:
            new_player_x: int = player_x
            new_player_y: int = player_y
            match move:
                case "<":
                    new_player_x -= 1
                case "v":
                    new_player_y += 1
                case ">":
                    new_player_x += 1
                case "^":
                    new_player_y -= 1
                case _:
                    pass

            if new_player_x < 0 or new_player_x >= self.width:
                continue
            if new_player_y < -1 or new_player_y > self.height:
                continue
            if new_player_y == -1 and new_player_x != self.entry_x:
                continue
            if new_player_y == self.height and new_player_x != self.exit_x:
                continue

            moves.append(move)
        return moves

    def draw(self, player_x: int = 0, player_y: int = -1) -> str:
        result: str = ""

        # top border
        for i in range(self.width + 2):
            if i == self.entry_x + 1:
                if player_y == -1:
                    result += "E"
                else:
                    result += "."
            else:
                result += "#"
        result += "\n"

        for i in range(self.height):
            line: str = ""
            for j in range(self.width):
                symbol: str = ""
                blizzard_count: int = 0
                if self.map[i][j] == 0:
                    symbol = "."
                if self.map[i][j] & 1:
                    symbol = "<"
                    blizzard_count += 1
                if self.map[i][j] & 2:
                    symbol = "v"
                    blizzard_count += 1
                if self.map[i][j] & 4:
                    symbol = ">"
                    blizzard_count += 1
                if self.map[i][j] & 8:
                    symbol = "^"
                    blizzard_count += 1
                if blizzard_count > 1:
                    symbol = str(blizzard_count)
                if i == player_y and j == player_x:
                    if blizzard_count > 0:
                        symbol = "X"
                    else:
                        symbol = "E"
                line += symbol
            result += "#" + line + "#\n"

        # bottom border
        for i in range(self.width + 2):
            if i == self.exit_x + 1:
                if player_y == self.height:
                    result += "E"
                else:
                    result += "."
            else:
                result += "#"
        result += "\n"

        return result