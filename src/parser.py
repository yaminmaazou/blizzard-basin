def parse(input_str: str) -> tuple[list[list[int]], int, int]:
    input_str = input_str.strip()
    lines: list[str] = input_str.split("\n")
    line_length: int = len(lines[0])
    map_str: list[str] = list(map(lambda x: x.strip("#"), lines[1:-1])) # remove the wall

    if len(lines) < 3:
        print("Error: File must contain at least three lines.")
        quit()
    if not all(len(line) == line_length for line in lines):
        print("Error: All lines must be of the same length.")
        quit()
    if not all(line.startswith("#") and line.endswith("#") for line in lines):
        print("Error: All lines must start and end with '#' characters.")
        quit()
    if lines[0].count(".") != 1:
        print("Error: The first line must contain a single '.' character.")
        quit()
    if lines[-1].count(".") != 1:
        print("Error: The last line must contain a single '.' character.")
        quit()
    if not all(c == "#" for c in lines[0].replace(".", "")):
        print("Error: The first line must consist of '.' and '#' characters only.")
        quit()
    if not all(c == "#" for c in lines[-1].replace(".", "")):
        print("Error: The last line must consist of '.' and '#' characters only.")
        quit()
    if not all(c in ".<>^v" for line in map_str for c in line):
        print("Error: Map can only contain '.', '<', '>', '^', and 'v'.")
        quit()

    entry_x: int = lines[0].index(".") - 1  # y is always -1
    exit_x: int = lines[-1].index(".") - 1

    map_int: list[list[int]] = []
    for line in map_str:
        new_line: list[int] = []
        for c in line:
            if c == "<":
                new_line.append(1)
            elif c == "v":
                new_line.append(2)
            elif c == ">":
                new_line.append(4)
            elif c == "^":
                new_line.append(8)
            else:
                new_line.append(0)
        map_int.append(new_line)
    
    return map_int, entry_x, exit_x