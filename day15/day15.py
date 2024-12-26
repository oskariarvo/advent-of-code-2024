import pandas as pd
# Animation module copied from shaansheikh: https://gist.github.com/shaansheikh/6336238447ea2e351d0aa395e748d03a
from warehouse_visualizer import WarehouseVisualizer

test_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
test_data = test_data.strip().split("\n")

test_data2 = """#######
#.....#
#..O..#
#@OO..#
#.....#
#...#.#
#######

>>^^>>vvvv>>^^"""
test_data2 = test_data2.strip().split("\n")

test_data3 = """##########
#........#
#........#
#........#
#........#
#...O@...#
#........#
#........#
#........#
##########

<^<vvvvvvvvv"""
test_data3 = test_data3.strip().split("\n")

test_data4 = """#####
#...#
#.O.#
#.O@#
#OO.#
#...#
#####

<>^<^<vv"""
test_data4 = test_data4.strip().split("\n")

with open("aoc-day15-input.txt", "r") as file:
    data = file.read().strip().split("\n")

# Clean input to a usable form which is pandas dataframe and string of movement characters
def clean_data(data, part):
    mapping = [value for value in data if "#" in value]
    if part == "part1":
        df_mapping = [list(x) for x in mapping]
        df = pd.DataFrame(df_mapping)
    elif part == "part2":
        new_mapping = []
        for item in mapping:
            new_row = ""
            for char in item:
                if char == "#":
                    new_row += "##"
                elif char == "O":
                    new_row += "[]"
                elif char == ".":
                    new_row += ".."
                elif char == "@":
                    new_row += "@."
            new_mapping.append(new_row)
        df_mapping = [list(x) for x in new_mapping]
        df = pd.DataFrame(df_mapping)

    move_chars = "v<^>"
    filtered_data = [row for row in data if any(char in row for char in move_chars)]
    joined_data = "".join(filtered_data)
    return df, joined_data


# Used to get new coordinates from old coordinates and direction
def add_coords(a, b):
        added = tuple(a + b for a, b in zip(a, b))
        return added

# Check that are there boxes or not / part 1
def check_boxes(df, current, direction):
    moved = add_coords(current, direction)
    if df.loc[moved] == "O":
        to_move = check_boxes(df, moved, direction)
        if to_move == True:
            df.loc[moved] = "."
            df.loc[add_coords(moved, direction)] = "O"
            return True
        else:
            return False
    elif df.loc[moved] == "#":
        return False
    elif df.loc[moved] == ".":
        return True

# Check that are there LARGE boxes or not / part 2
def check_double_boxes(df, current, direction, move, store):
    # West or east movement works pretty much the same as in part 1
    if move == ">" or move == "<":
        moved = add_coords(current, direction)
        if df.loc[moved] == "[":
            to_move = check_double_boxes(df, moved, direction, move, store)
            if to_move == True:
                df.loc[moved] = "."
                df.loc[add_coords(moved, direction)] = "["
                return True
            else:
                return False
        elif df.loc[moved] == "]":
            to_move = check_double_boxes(df, moved, direction, move, store)
            if to_move == True:
                df.loc[moved] = "."
                df.loc[add_coords(moved, direction)] = "]"
                return True
            else:
                return False
        elif df.loc[moved] == "#":
            return False
        elif df.loc[moved] == ".":
            return True
    # North south movement is a bit trickier using recursion.
    # Idea here is that we return values of what is in front of the last boxes.
    # If there is a # or a wall we return (-1, -1) and if there is a . or dot we return that coordinate.
    elif move == "^" or move == "v":
        moved = add_coords(current, direction)
        if df.loc[moved] == "[":
            to_move = check_double_boxes(df, moved, direction, move, store)
            to_move = check_double_boxes(df, add_coords(moved,(0, 1)), direction, move, store)
            if to_move == True:
                return True
            else:
                return False
        elif df.loc[moved] == "]":
            to_move = check_double_boxes(df, moved, direction, move, store)
            to_move = check_double_boxes(df, add_coords(moved,(0, -1)), direction, move, store)
            if to_move == True:
                return store
            else:
                return store
        elif move == "^":
            if (df.loc[moved] == "#"):
                store.append((-1, -1))
                return False
            elif df.loc[moved] == "." and len(store) == 0:
                store.append(moved)
                return True
        elif move == "v":
            if (df.loc[moved] == "#"):
                store.append((-1, -1))
                return False
            elif df.loc[moved] == ".":
                store.append(moved)
                return True

# Move robot according to store which lists all possible vertical movements from check_double_boxes
# This function works largely like the check_double_boxes function. The reason that we check first
# is because recursive functions work seperately and might not check lists globally while executing.
# That depends on the order of the recursive functions.
#
# So first we check if it is possible to move the large boxes with check_double_boxes and then move them with this function
def move_boxes(df, current, direction, move):
    moved = add_coords(current, direction)
    if df.loc[moved] == "[":
        to_move = move_boxes(df, moved, direction, move)
        to_move = move_boxes(df, add_coords(moved,(0, 1)), direction, move)
        if to_move == True:
            df.loc[moved] = "."
            new_dot = add_coords(moved, (0, 1))
            new_box = add_coords(moved, direction)
            df.loc[new_box] = "["
            df.loc[add_coords(new_box, (0, 1))] = "]"
            df.loc[new_dot] = "."
            return True
        else:
            return False
    elif df.loc[moved] == "]":
        to_move = move_boxes(df, moved, direction, move)
        to_move = move_boxes(df, add_coords(moved,(0, -1)), direction, move)
        if to_move == True:
            df.loc[moved] = "."
            new_dot = add_coords(moved, (0, -1))
            new_box = add_coords(moved, direction)
            df.loc[new_box] = "]"
            df.loc[add_coords(new_box, (0, -1))] = "["
            df.loc[new_dot] = "."
            return True
        else:
            return False
    elif move == "^":
        if (df.loc[moved] == "#"):
            return False
        elif df.loc[moved] == ".":
            return True
    elif move == "v":
        if (df.loc[moved] == "#"):
            return False
        elif df.loc[moved] == ".":
            return True

# Used to make a list format grid so we can use it in our animation
def for_animation(df):
    grid = []
    new_string = []
    for index, row in df.iterrows():
        for col in df.columns:
            new_string.append(row[col])
        grid.append(new_string)
        new_string = []
    return grid

# Move robot according to input
def move_robot(cleaned):
    CURSOR_UP = "\033[F"
    visualizer = WarehouseVisualizer()
    df = cleaned[0]
    # Track robot initial position
    for index, row in df.iterrows():
        for col in df.columns:
            if row[col] == "@":
                current = index, col
                # print("Initial:" + str(current))
                print(current)
    moves = cleaned[1]
    directions = dict()
    directions["v"] = (1, 0)
    directions["<"] = (0, -1)
    directions["^"] = (-1, 0)
    directions[">"] = (0, 1)
    count = 0
    for move in moves:
        count += 1
        # Keep track how many moves we have been through
        print(CURSOR_UP + str(count) + " / " + str(len(moves)))
        moved = add_coords(current, directions[move])
        # Used in part 1
        if df.loc[moved] == "O":
            to_move = check_boxes(df, current, directions[move])
            if to_move == True:
                df.loc[current] = "."
                df.loc[moved] = "@"
                current = moved
            else:
                continue
        # Used in part 2
        elif df.loc[moved] == "[" or df.loc[moved] == "]":
            store = list()
            to_move = check_double_boxes(df, current, directions[move], move, store)
            if ((-1, -1) not in store) and len(store) != 0:
                move_boxes(df, current, directions[move], move)
                df.loc[current] = "."
                df.loc[moved] = "@"
                current = moved
            elif to_move == True and len(store) == 0:
                df.loc[current] = "."
                df.loc[moved] = "@"
                current = moved
            else:
                continue
        # If there is a wall straight ahead --> skip
        elif df.loc[moved] == "#":
            continue
        # If there is a free space or dot straight ahead --> move there
        elif df.loc[moved] == ".":
            df.loc[current] = "."
            df.loc[moved] = "@"
            current = moved
        # Uncomment below if you want to see animation
        # grid = for_animation(df)
        # visualizer.show_frame(grid, 0.1)

    # Return the rearranged dataframe
    return df

# Count the boxes coordinates
def count_GPS(df):
    total = 0
    for index, row in df.iterrows():
        for col in df.columns:
            if row[col] == "O" or row[col] == "[":
                total += 100 * index + col
                #print(total)
    return total

# Test for part 1
print("Part 1 test:")
test_data_part1 = clean_data(test_data, "part1")
test_boxes_part1 = move_robot(test_data_part1)
print(count_GPS(test_boxes_part1))
print("\n")

# Actual part 1
print("Part 1:")
cleaned_data_part1 = clean_data(data, "part1")
arranged_boxes_part1 = move_robot(cleaned_data_part1)
print(count_GPS(arranged_boxes_part1))
print("\n")

# Test for part 2
print("Part 2 test:")
test_data_part2 = clean_data(test_data, "part2")
test_boxes_part2 = move_robot(test_data_part2)
print(count_GPS(test_boxes_part2))
print("\n")

# Actual part 2
print("Part 2:")
cleaned_data_part2 = clean_data(data, "part2")
arranged_boxes_part2 = move_robot(cleaned_data_part2)
print(count_GPS(arranged_boxes_part2))