import numpy as np
import re
from collections import defaultdict

# Test data
test_data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
test_data = test_data.strip().split("\n")
test_arr = np.array(test_data)

# Actual data
with open("aoc-day14-input.txt", "r") as file:
    data = file.read().strip().split("\n")
arr = np.array(data)

def clean_data(data):
    def extract_numbers(item):
        return list(map(int, re.findall(r"[+-]?\d+", item)))
    vectorized_extract = np.vectorize(extract_numbers, otypes=[object])
    cleaned_data = vectorized_extract(data)
    return cleaned_data

# Cleaned data for further use
test_cleaned_data = clean_data(test_arr)
cleaned_data = clean_data(arr)

# Move data certain velocity in certain time
def calc_future(data, secs, tiles):
    move = (data[2] * secs), (data[3] * secs)
    position = (data[0] + move[0]) % tiles[0], (data[1] + move[1]) % tiles[1]
    return position

# Count safety factor
def safety_factor(data, secs, tiles):
    all_coords = defaultdict(int)
    for item in data:
        coord = calc_future(item, secs, tiles)
        if coord[0] != (tiles[0] // 2) or coord[0] != (tiles[1] // 2):
            if (0 <= coord[0] < (tiles[0] // 2)) and (0 <= coord[1] < (tiles[1] // 2)):
                all_coords["1"] += 1
            elif ((tiles[0] // 2) < coord[0] < (tiles[0])) and (0 <= coord[1] < (tiles[1] // 2)):
                all_coords["2"] += 1
            elif (0 <= coord[0] < (tiles[0] // 2)) and ((tiles[1] // 2) < coord[1] < (tiles[1])):
                all_coords["3"] += 1
            elif ((tiles[0] // 2) < coord[0] < (tiles[0])) and ((tiles[1] // 2) < coord[1] < (tiles[1])):
                all_coords["4"] += 1
    factor = 0
    for value in all_coords.values():
        if factor == 0:
            factor = value
        else:
            factor *= value
    return factor

# Find christmas tree using brute force
def brutus_check(data, tiles):
    secs = 0
    tree_x = None
    while True:
        if tree_x != None:
            secs += 103
        else:
            secs += 1
        tree_y = -2
        robots = set()
        # Move robots according to seconds
        for item in data:
            moved = calc_future(item, secs, tiles)
            robots.add(moved)
        # Find in which value the x arranges so we can iterate every 103 second
        if tree_x == None:
            for x in range(tiles[1]):
                total_x = 0
                for value in robots:
                    if value[1] == x:
                        total_x += 1
                if total_x > 15:
                    tree_x = secs
        # Find if y values arrange themselves
        for y in range(tiles[0]):
            total_y = 0
            for value in robots:
                if value[0] == y:
                    total_y += 1
            if total_y > 15:
                tree_y = secs
        # If both x and y arranges we have a christmas tree
        if tree_y == secs:
            print(secs)
            break

# Find christmas tree using chinese remainder theorem
def remainder_check(data, tiles):
    secs = 0
    tree_x = None
    tree_y = None
    while True:
        secs += 1
        robots = set()
        # Move robots according to seconds
        for item in data:
            moved = calc_future(item, secs, tiles)
            robots.add(moved)
        # Find in which value the x arranges so we can iterate every 103 second
        if tree_x == None:
            for x in range(tiles[1]):
                total_x = 0
                for value in robots:
                    if value[1] == x:
                        total_x += 1
                if total_x > 15:
                    tree_x = secs
        # Find if y values arrange themselves
        for y in range(tiles[0]):
            total_y = 0
            for value in robots:
                if value[0] == y:
                    total_y += 1
            if total_y > 15:
                tree_y = secs
        # Find the christmas tree using Chinese Remainder Theorem
        if tree_y != None and tree_x != None:
            j = tiles[1] % tiles[0]
            i = abs((tree_y % tiles[0]) - (tree_x % tiles[0]))
            if j > 1:
                x = (1-tiles[0]) / 2
                while x <= 0:
                    x += tiles[0]
                j = (x * i) % tiles[0]
            else:
                j = i
            result = tiles[1]*j+tree_x
            print(int(result))
            break
    
# Part 1
print(safety_factor(test_cleaned_data, 100, (11, 7)))
print(safety_factor(cleaned_data, 100, (101, 103)))
# Part 2
brutus_check(cleaned_data, (101, 103))
remainder_check(cleaned_data, (101, 103))