import pandas as pd
# Animation module copied from shaansheikh: https://gist.github.com/shaansheikh/6336238447ea2e351d0aa395e748d03a
from warehouse_visualizer import WarehouseVisualizer
from collections import Counter
import time

test_data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

test_data2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

# Insert all inputs into a pandas dataframe for easier handling in the future
test_data = test_data.strip().split("\n")
chars = [list(line) for line in test_data]
test_df = pd.DataFrame(chars)

test_data2 = test_data2.strip().split("\n")
chors = [list(line) for line in test_data2]
test2_df = pd.DataFrame(chors)

with open("aoc-day16-input.txt", "r") as file:
    data = file.read().strip().split("\n")
rows = [list(line) for line in data]
df = pd.DataFrame(rows)


# Used to get new coordinates from old coordinates and direction
def add_coords(a, b):
    #Parameters:
    #@a tuple (int, int): a tuple we can add together
    #@b tuple (int, int): a tuple we can add together
    #Returns:
    #tuple: The tuples added together
        added = tuple(a + b for a, b in zip(a, b))
        return added

# Used to make dataframe into grid format so we can use it in our animation module
def for_animation(df):
    #Parameters:
    #@df dataframe: Dataframe we make into the grid
    #Returns:
    #list of strings: We can use this format in our animation module
    grid = []
    new_string = []
    for index, row in df.iterrows():
        for col in df.columns:
            new_string.append(row[col])
        grid.append(new_string)
        new_string = []
    return grid

# Count the final scores from our path finding function
def count_score(found_list, turns, part):
    #Parameters:
    #@found_list tuple ((int, int), int, set()): Tuple format which we can count the final score for part 1 and 2
    #@turns int: The number with which we can calculate the final score for part 1
    #@part string: Which part do we want to solve
    #Returns:
    #int: Get the final score for the answer
    if part == "part1":
        minimal = 1000000
        for each in found_list:
            if each[1] < minimal:
                minimal = each[1]
        return turns * 1000 + minimal
    elif part == "part2":
        final_set = set()
        for path in found_list:
            final_set.update(path[2])
        return len(final_set)

# Check for duplicates in a list, if there is one -> choose the one with the lowest steps
# This function is used to make the program more memory efficient
def check_for_duplicates(the_list, part):
    #Parameters:
    #@found_list tuple ((int, int), int, set()): Tuple format which we can check for duplicates in parts 1 and 2
    #@part string: Which part do we want to solve
    #Returns:
    #tuple ((int, int), int, set()): Get a new list processed and rid of duplicates
    only_coords = []
    for each in the_list:
        only_coords.append(each[0])
    counter = Counter(only_coords)
    duplicates = [item for item, count in counter.items() if count > 1]
    if len(duplicates) != 0:
        filtered_list = []
        for duplicate in duplicates:
            indexes = [i for i, value in enumerate(only_coords) if value == duplicate]
            all_steps = []
            if part == "part2":
                duplicate_set = set()
            for i in indexes:
                all_steps.append(the_list[i][1])
            minimal_coord = min(all_steps)
            if part == "part2":
                for i in indexes:
                    diff = abs(the_list[i][1] - minimal_coord)
                    if diff == 0:
                        duplicate_set.update(the_list[i][2])
                filtered_list.append((duplicate, minimal_coord, duplicate_set))
            if part == "part1":
                filtered_list.append((duplicate, minimal_coord))
        singular = [item for item, count in counter.items() if count == 1]
        for single in singular:
            index = [i for i, value in enumerate(only_coords) if value == single]
            filtered_list.append(the_list[index[0]])
        the_list = filtered_list
    return the_list

# Used to make beams or looking at all the rows and columns where there is a turning point, and saving them.
# Then make new beams in the different angle, and continue this looping process until we have a beam that is on the end coordinate.
def beam(df, the_list, direction, visited, end_pos, part):
    #Parameters:
    #@df dataframe: We can check for patterns in the dataframe
    #@the_list list of tuples ((int, int), int, set()): Tuple format which we can check for possible turns next to the beam
    #@direction int: Are we going sideways or up-and-down direction: 1 is for up-and-down, 0 is for sideways
    #@visited set(): Which turns or coordinates have we already been through
    #@end_pos tuple (int, int): What is the E or end point we want to reach
    #@part string: Which part do we want to solve
    #Returns:
    #new_list list of tuples ((int, int), int, set()): Get the turn points for new beam and been to positions for part 2
    #found_list list of tuples ((int, int), int, set()): If beam reaches E this will returns the beam the that reached it and been to positions for part 2
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    new_list = []
    found_list = []
    # if beam is 
    if direction == 1:
        first = 2
        second = 0
        side = 1
        otherside = 3
    else:
        first = 3
        second = 1
        side = 0
        otherside = 2
    for each in the_list:
        if part == "part2":
            all_paths = each[2].copy()
        steps = each[1]
        current_pos = each[0]
        current_pos = add_coords(current_pos, directions[first])
        steps += 1
        while df.loc[current_pos] != "#":
            if part == "part2":
                all_paths.add(current_pos)
            if (df.loc[add_coords(current_pos, directions[side])] == "." or df.loc[add_coords(current_pos, directions[otherside])] == ".") and (current_pos) not in visited:
                if part == "part1":
                    new_list.append((current_pos, steps))
                elif part == "part2":
                    new_list.append((current_pos, steps, all_paths.copy()))
            if current_pos == end_pos:
                if part == "part1":
                    found_list.append((current_pos, steps))
                elif part == "part2":
                    found_list.append((current_pos, steps, all_paths.copy()))

            current_pos = add_coords(current_pos, directions[first])
            steps += 1
        if part == "part2":
            all_paths = each[2].copy()
        steps = each[1]
        current_pos = each[0]
        current_pos = add_coords(current_pos, directions[second])
        steps += 1
        while df.loc[current_pos] != "#":
            if part == "part2":
                all_paths.add(current_pos)
            if (df.loc[add_coords(current_pos, directions[side])] == "." or df.loc[add_coords(current_pos, directions[otherside])] == ".") and (current_pos) not in visited:
                if part == "part1":
                    new_list.append((current_pos, steps))
                elif part == "part2":
                    new_list.append((current_pos, steps, all_paths.copy()))
            if current_pos == end_pos:
                if part == "part1":
                    found_list.append((current_pos, steps))
                elif part == "part2":
                    found_list.append((current_pos, steps, all_paths.copy()))

            current_pos = add_coords(current_pos, directions[second])
            steps += 1
    return new_list, found_list


def find_path_beams(df, part):
    visualizer = WarehouseVisualizer()
    #Parameters:
    #@df dataframe: We solve input for the parts using this dataframe format
    #@part string: Which part do we want to solve
    #Returns:
    #int: Depending on the part this returns the solved values for both parts
    for index, row in df.iterrows():
            for col in df.columns:
                if row[col] == "S":
                    start_pos = index, col
                    print("S:" + str(start_pos))
                if row[col] == "E":
                    end_pos = index, col
                    print("E:" + str(end_pos))
    vertical_list = []
    horizontal_list = []
    turns = 0
    found_list = []
    visited = set()
    if part == "part2":
        all_paths = set()
    while True:
        # Animation module:
        # grid = for_animation(df)
        # visualizer.show_frame(grid, 0.2)
        if turns == 0:
            current_pos = start_pos
            steps = 0
            if part == "part2":
                all_paths = set()
            while df.loc[current_pos] != "#":
                if part == "part2":
                    all_paths.add(current_pos)
                if (df.loc[add_coords(current_pos, (1, 0))] == "." or df.loc[add_coords(current_pos, (-1, 0))] == ".") and (current_pos) not in visited:
                    if part == "part1":
                        vertical_list.append((current_pos, steps))
                    elif part == "part2":
                        vertical_list.append((current_pos, steps, all_paths.copy()))
                if current_pos == end_pos:
                    if part == "part1":
                        found_list.append((current_pos, steps))
                    elif part == "part2":
                        found_list.append((current_pos, steps, all_paths.copy()))
                current_pos = add_coords(current_pos, (0, 1))
                steps += 1
            current_pos = start_pos
            steps = 2001
            if part == "part2":
                all_paths = set()
            current_pos = add_coords(current_pos, (0, -1))
            while df.loc[current_pos] != "#":
                if part == "part2":
                    all_paths.add(current_pos)
                if (df.loc[add_coords(current_pos, (1, 0))] == "." or df.loc[add_coords(current_pos, (-1, 0))] == ".") and (current_pos) not in visited:
                    if part == "part1":
                        vertical_list.append((current_pos, steps))
                    elif part == "part2":
                        vertical_list.append((current_pos, steps, all_paths.copy()))
                if current_pos == end_pos:
                    if part == "part1":
                        found_list.append((current_pos, steps))
                    elif part == "part2":
                        found_list.append((current_pos, steps, all_paths.copy()))
                current_pos = add_coords(current_pos, (0, -1))
                steps += 1
            vertical_list = check_for_duplicates(vertical_list, part)
            for each in vertical_list:
                visited.add(each[0])
        if turns % 2 == 1:
            horizontal_list, found_list = beam(df, vertical_list, 1, visited, end_pos, part)
            vertical_list = []
            horizontal_list = check_for_duplicates(horizontal_list, part)
            for each in horizontal_list:
                visited.add(each[0])

        elif turns % 2 == 0 and turns != 0:
            vertical_list, found_list = beam(df, horizontal_list, 0, visited, end_pos, part)
            horizontal_list = []
            vertical_list = check_for_duplicates(vertical_list, part)
            for each in vertical_list:
                visited.add(each[0])

        if len(found_list) != 0:
            break
        turns += 1
    if part == "part1":
        return count_score(found_list, turns, part)
    elif part == "part2":
        return count_score(found_list, turns, part)


# # part 1
# print(find_path_beams(test_df, "part1"))
# print(find_path_beams(test2_df, "part1"))
# print(find_path_beams(df, "part1"))

# # part 2
# print(find_path_beams(test_df, "part2"))
# print(find_path_beams(test2_df, "part2"))
# print(find_path_beams(df, "part2"))

# To run this program and solve the parts
if __name__ == "__main__":
    print("Part 1:")
    start_time = time.time()
    print("Result:", find_path_beams(df, "part1"))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time, "seconds")
    print("\nPart 2:")
    start_time = time.time()
    print("Result:", find_path_beams(df, "part2"))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time, "seconds")