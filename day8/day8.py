import pandas as pd
import itertools

grid = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

# Making test data into dataframe
chars = grid.strip().split("\n")
eachchars = [list(row) for row in chars]
pf = pd.DataFrame(eachchars)

# Making actual data into dataframe
with open("aoc-day8-input.txt", "r") as file:
    data = file.read().strip().split("\n")
rows = [list(line) for line in data]
df = pd.DataFrame(rows)

# Count the two possible antinode locations
def count_antinodes(a, b):
        bigger = max(a, b)
        smaller = min(a, b)
        difference = tuple(abs(bigger - smaller) for bigger, smaller in zip(bigger, smaller))
        if smaller[1] > bigger[1]:
            backwards = (smaller[0] - difference[0], smaller[1] + difference[1])
            forwards = (bigger[0] + difference[0], bigger[1] - difference[1])
        else: 
            backwards = (smaller[0] - difference[0], smaller[1] - difference[1])
            forwards = (bigger[0] + difference[0], bigger[1] + difference[1])
        return backwards, forwards, difference

# Count the all possible antinode locations
def count_antinodes_part2(a, b, df):
        antinodes = set()
        bigger = max(a, b)
        smaller = min(a, b)
        difference = tuple(abs(bigger - smaller) for bigger, smaller in zip(bigger, smaller))
        backwards = smaller
        forwards = bigger
        antinodes.add(backwards)
        antinodes.add(forwards)
        if smaller[1] > bigger[1]:
            while (0 <= backwards[0] < len(df) and 0 <= backwards[1] < len(df.columns)):
                backwards = (backwards[0] - difference[0], backwards[1] + difference[1])
                antinodes.add(backwards)
            while (0 <= forwards[0] < len(df) and 0 <= forwards[1] < len(df.columns)):
                forwards = (forwards[0] + difference[0], forwards[1] - difference[1])
                antinodes.add(forwards)
        else: 
            while (0 <= backwards[0] < len(df) and 0 <= backwards[1] < len(df.columns)):
                backwards = (backwards[0] - difference[0], backwards[1] - difference[1])
                antinodes.add(backwards)
            while (0 <= forwards[0] < len(df) and 0 <= forwards[1] < len(df.columns)):
                forwards = (forwards[0] + difference[0], forwards[1] + difference[1])
                antinodes.add(forwards)
        return antinodes

def antinodes(df):

    # Creating dictionary and initial coordinates
    allChars = dict()
    y = -1

    # Saving all the coordinates of antennas
    for index, row in df.iterrows():
        x = -1
        y += 1
        for item in row:
            x += 1
            if item != ".":
                if item in allChars.keys():
                    allChars[item].append((y, x))
                else:
                    allChars[item] = []
                    allChars[item].append((y, x))

    # Count all antinodes
    count = set()
    for key, value in allChars.items():   
        combinations = itertools.combinations(value, 2)
        combs = list(combinations)
        for comb in combs:
            coords = count_antinodes(comb[0], comb[1])
            if (0 <= (coords[0][0]) < len(df) and 0 <= coords[0][1] < len(df.columns)) and coords[0] not in count:
                count.add(coords[0])
                # if df.loc[coords[0]] == ".":
                #     df.loc[coords[0]] = "#"
            if (0 <= (coords[1][0]) < len(df) and 0 <= coords[1][1] < len(df.columns)) and coords[1] not in count:
                count.add(coords[1])
                # if df.loc[coords[1]] == ".":
                #     df.loc[coords[1]] = "#"
    return len(count)

def antinodes_part2(df):

    # Creating dictionary and initial coordinates
    allChars = dict()
    y = -1

    # Saving all the coordinates of antennas
    for index, row in df.iterrows():
        x = -1
        y += 1
        for item in row:
            x += 1
            if item != ".":
                if item in allChars.keys():
                    allChars[item].append((y, x))
                else:
                    allChars[item] = []
                    allChars[item].append((y, x))

    # Count all antinodes
    count = set()
    for key, value in allChars.items():   
        combinations = itertools.combinations(value, 2)
        combs = list(combinations)
        for comb in combs:
            coords = count_antinodes_part2(comb[0], comb[1], df)
            for each in coords:
                if (0 <= each[0] < len(df) and 0 <= each[1] < len(df.columns)) and each not in count:
                    count.add(each)
                    # if df.loc[each] == ".":
                    #     df.loc[each] = "#"
    return len(count)



# Test values
print(antinodes(pf))
print(antinodes_part2(pf))

# Actual values
print(antinodes(df))
print(antinodes_part2(df))