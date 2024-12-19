import pandas as pd

test_data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

test_data2 = """
..........
.###...##.
.^......#.
.##....###
.....##...
....#.....
.##.......
.#....####
.#...#....
..........
"""

test_data = test_data.strip().split("\n")

test_data2 = test_data2.strip().split("\n")


with open("aoc-day6-input.txt", "r") as file:
    data = file.read().strip().split("\n")

#print(data)
#rows = [line.split() for line in data]
rows = [list(line) for line in data]

chars = [list(line) for line in test_data]

chors = [list(line) for line in test_data2]

df = pd.DataFrame(rows)
#print(chars)

test_df = pd.DataFrame(chars)

test2_df = pd.DataFrame(chors)

#print(df)

def add_coords(a, b):
        added = tuple(a + b for a, b in zip(a, b))
        return added

def how_many_distinct(df):
    positions = [
        (-1, 0), # ylös
        (0, 1),  # oikealle
        (1, 0),  # alas
        (0, -1)  # vasemmalle
        ]

    total = 0

    for index, row in df.iterrows():
        for col in df.columns:
            if row[col] == "^":
                current = index, col
                print(current)
                print(df.loc[current])
                df.loc[current] = "X"

    i = 0
    position = positions[0]


    while (0 <= (current[0] + position[0]) < len(df)) and (0 <= (current[1] + position[1]) < len(df.columns)):
        # Change position
        print(current, position)
        if df.loc[add_coords(current, position)] == "#":
            i += 1
            if i == 4:
                i = 0
            position = positions[i]
        # Move character by one
        if not df.loc[current] == "X":
            total += 1
        current = add_coords(current, position)
        df.loc[current] = "X"
        print(df)
        print(current)

    for index, row in df.iterrows():
        for col in df.columns:
            if df.loc[index, col] == "X":
                total += 1
    return total



def how_many_distinct_obs(df):
    positions = [
        (-1, 0), # ylös
        (0, 1),  # oikealle
        (1, 0),  # alas
        (0, -1)  # vasemmalle
        ]
    ways = [
        "^", # ylös
        ">",  # oikealle
        "v",  # alas
        "<"  # vasemmalle
        ]

    total = 0
    visited = set()

    for index, row in df.iterrows():
        for col in df.columns:
            if row[col] == "^":
                star = index, col
                current = star
                print(current)
                print(df.loc[current])

    print(df)
    i = 0
    position = positions[0]
    way = ways[0]

    # def to_right(df, coords, Y):
    #     #print(coords)
    #     #df.loc[Y] = "#"
    #     #print(df)
    #     row = df.iloc[coords[0]]
    #     og_row = row
    #     row = row[coords[1]:]
    #     found = False
    #     new_coords = coords
    #     advance = False
    #     #print(row)
    #     if "#" in row.values:
    #         last_index = row.where(row == "#").first_valid_index() - 1
    #         new_coords = (coords[0], last_index)
    #         advance = True
    #         #print(last_index)
    #         row = og_row[coords[1]:last_index + 1]
    #         #print(row)
    #     if "Y" in row.values:
    #         #print(row)
    #         found = True
    #         advance = False
    #         Y_index = row.where(row == "Y").first_valid_index()
    #         new_coords = (coords[0], Y_index)
    #     return found, new_coords, advance

    # def to_down(df, coords, Y):
    #     #print(coords)
    #     #df.loc[Y] = "#"
    #     col = df[coords[1]]
    #     og_col = col
    #     col = col[coords[0]:]
    #     found = False
    #     new_coords = coords
    #     advance = False
    #     #print(col)
    #     if "#" in col.values:
    #         last_index = col.where(col == "#").first_valid_index() - 1
    #         new_coords = (last_index, coords[1])
    #         advance = True
    #         #print(last_index)
    #         # print("column")
    #         col = og_col[coords[0]:last_index + 1]
    #         #print(col)
    #     if "Y" in col.values:
    #         found = True
    #         advance = False
    #         Y_index = col.where(col == "Y").first_valid_index()
    #         new_coords = (Y_index, coords[1])
    #     return found, new_coords, advance
    
    # def to_left(df, coords, Y):
    #     #print(coords)
    #     #df.loc[Y] = "#"
    #     row = df.iloc[coords[0]]
    #     og_row = row
    #     row = row[:coords[1] + 1]
    #     found = False
    #     new_coords = coords
    #     advance = False
    #     #print(row)
    #     if "#" in row.values:
    #         last_index = row.where(row == "#").last_valid_index() + 1
    #         new_coords = (coords[0], last_index)
    #         advance = True
    #         #print(last_index)
    #         row = og_row[last_index:coords[1] + 1]
    #         #print(row)
    #     if "Y" in row.values:
    #         found = True
    #         advance = False
    #         Y_index = row.where(row == "Y").last_valid_index()
    #         new_coords = (coords[0], Y_index)
    #     #print(df)
    #     return found, new_coords, advance
    
    # def to_up(df, coords, Y):
    #     #df.loc[Y] = "#"
    #     col = df[coords[1]]
    #     og_col = col
    #     col = col[:coords[0] + 1]
    #     found = False
    #     new_coords = coords
    #     advance = False
    #     #print(col)
    #     if "#" in col.values:
    #         last_index = col.where(col == "#").last_valid_index() + 1
    #         new_coords = (last_index, coords[1])
    #         advance = True
    #         #print(last_index)
    #         #print("column")
    #         col = og_col[last_index:coords[0]]
    #         #print(col)
    #     if "Y" in col.values:
    #         found = True
    #         advance = False
    #         Y_index = col.where(col == "Y").last_valid_index()
    #         new_coords = (Y_index, coords[1])
    #     return found, new_coords, advance



    def check_loop(df, coords, i, positions):
        # keep track of visited positions (coordinates, direction)
        visited_loop = set()

        # which direction are we currently going
        direction = positions[i]
        # add obstacle
        obs = add_coords(coords, direction)
        #print("obs coords:", obs)
        df.loc[obs] = "#"

        while (0 <= (coords[0] + direction[0]) < len(df)) and (0 <= (coords[1] + direction[1]) < len(df.columns)):
            
            # check for visited, if visited already, then there is a loop
            if (coords[0], coords[1], direction[0], direction[1]) in visited_loop:
                df.loc[obs] = "."
                print("there is a loop", coords, direction)
                return True
            
            # add to visited positions
            visited_loop.add((coords[0], coords[1], direction[0], direction[1]))

            # turn if there is a wall in front
            while df.loc[add_coords(coords, direction)] == "#":
                i += 1
                i = i % 4
                direction = positions[i]
            
            # increment/move ahead
            coords = add_coords(coords, direction)
        print("no loop")
        df.loc[obs] = "."
        return False




    # def start(df, coords, Y, i, on_ollut):
    #     #found = False
    #     og_coords = coords
    #     df.loc[Y] = "Y"
    #     if Y in on_ollut:
    #         return False, og_coords

    #     #print(df)
    #     j = 0
    #     #print("Y:", Y)

    #     while (True):
    #         #print(i)
    #         if i == 0:
    #             #print(coords)
    #             result = to_right(df, coords, Y)
    #             coords = result[1]
    #             #print("res1:", result)
    #             if result[0]:
    #                 return True, coords
    #             if result[2] == False:
    #                 return False, coords
    #         elif i == 1:
    #             #print(coords)
    #             result = to_down(df, coords, Y)
    #             coords = result[1]
    #             #print("res2:", result)
    #             if result[0]:
    #                 return True, coords
    #             if result[2] == False:
    #                 return False, coords
    #         elif i == 2:
    #             #print(coords)
    #             result = to_left(df, coords, Y)
    #             coords = result[1]
    #             #print("res3:", result)
    #             if result[0]:
    #                 return True, coords
    #             if result[2] == False:
    #                 return False, coords
    #         elif i == 3:
    #             #print(coords)
    #             result = to_up(df, coords, Y)
    #             coords = result[1]
    #             #print("res4:", result)
    #             if result[0]:
    #                 return True, coords
    #             if result[2] == False:
    #                 return False, coords

    #         i += 1

    #         i = i % 4

    #         j += 1
    #         #print(j)
    #         #print(coords)

    #         if j > 1000:
    #             return True, og_coords

    #         #print("waaa")
    #         #return found, coords
    


    while (0 <= (current[0] + position[0]) < len(df)) and (0 <= (current[1] + position[1]) < len(df.columns)):
        # Change position
        print("current:", current, position)
        #print("????")
        if len(visited) == 0:
            visited.add(current)
            #print(on_ollut)
        elif df.loc[add_coords(current, position)] == "#":
            i += 1
            if i == 4:
                i = 0
            position = positions[i]
            way = ways[i]
            df.loc[current] = way
        else:
        # Move character by one
            current = add_coords(current, position)
            visited.add(current)
            df.loc[current] = way

        if (0 <= (current[0] + position[0]) < len(df)) and (0 <= (current[1] + position[1]) < len(df.columns)):
            if (df.loc[add_coords(current, position)] == "."):
                result = check_loop(df, current, i, positions)
                if result == True:
                    total += 1

    print(total)
    print(df)
    return total

#print(how_many_distinct(test_df))

print(how_many_distinct_obs(df))
