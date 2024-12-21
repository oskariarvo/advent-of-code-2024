import pandas as pd

grid = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

# Making test data into dataframe
chars = grid.strip().split("\n")
eachchars = [list(row) for row in chars]
pf = pd.DataFrame(eachchars)

# Making actual data into dataframe
with open("aoc-day10-input.txt", "r") as file:
    data = file.read().strip().split("\n")
rows = [list(line) for line in data]
df = pd.DataFrame(rows)

# Finding all zeros or starting pos in data
def find_starting_pos(df):
    start_positions = []
    y = -1
    for index, row in df.iterrows():
        y += 1
        x = -1
        for coord in row:
            x += 1
            if coord == "0":
                start_positions.append((y, x))
    return start_positions

# Add two coordinates, used in direction change
def add_coords(a, b):
        added = tuple(a + b for a, b in zip(a, b))
        return added

# Move one to each possible direction
def move_one(coord, df):
    all_possible = []
    positions = [
        (-1, 0), # ylös
        (0, 1),  # oikealle
        (1, 0),  # alas
        (0, -1)  # vasemmalle
        ]
    for pos in positions:
        current_value = df.loc[coord]
        coords = add_coords(pos, coord)
        if (0 <= coords[0] < len(df) and 0 <= coords[1] < len(df.columns)):
            possible_value = df.loc[coords]
            if (int(possible_value)-int(current_value) == 1):
                all_possible.append(coords)
    return all_possible

# Finding all trails
def find_trails(start_pos_list, df, all_nines=None):
    total = 0
    for start_pos in start_pos_list:
        if all_nines is None or df.loc[start_pos] == "0":
            all_nines = set()
        current_coord = start_pos
        while current_coord != (-1, -1):
            if df.loc[current_coord] == "9":
                if current_coord not in all_nines:
                    total += 1
                all_nines.add(current_coord)
                break

            current_coord_list = move_one(current_coord, df)

            if len(current_coord_list) > 1:
                total += find_trails(current_coord_list, df, all_nines)
                current_coord = (-1, -1)
            elif len(current_coord_list) == 1:
                current_coord = current_coord_list[0]
            else:
                current_coord = (-1, -1)
    return total

# Find distinct trails / only changed if condition into a comment
def find_distinct_trails(start_pos_list, df, all_nines=None):
    total = 0
    for start_pos in start_pos_list:
        if all_nines is None or df.loc[start_pos] == "0":
            all_nines = set()
        current_coord = start_pos
        while current_coord != (-1, -1):
            if df.loc[current_coord] == "9":
                #if current_coord not in all_nines:
                total += 1
                all_nines.add(current_coord)
                break

            current_coord_list = move_one(current_coord, df)

            if len(current_coord_list) > 1:
                total += find_distinct_trails(current_coord_list, df, all_nines)
                current_coord = (-1, -1)
            elif len(current_coord_list) == 1:
                current_coord = current_coord_list[0]
            else:
                current_coord = (-1, -1)
    return total


def hoof_it_part1(df):
    positions = find_starting_pos(df)
    return find_trails(positions, df)

def hoof_it_part2(df):
    positions = find_starting_pos(df)
    return find_distinct_trails(positions, df)

print(hoof_it_part1(pf))
print(hoof_it_part1(df))

print(hoof_it_part2(pf))
print(hoof_it_part2(df))
