import numpy as np
import re

# Test data
test_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
test_data = test_data.strip().split("\n")
test_arr = np.array(test_data)
test_indices = np.where(test_arr == "")[0]
test_result = np.split(test_arr, test_indices + 1)
test_result = [list(x[x != ""]) for x in test_result]

# Actual data
with open("aoc-day13-input.txt", "r") as file:
    data = file.read().strip().split("\n")
arr = np.array(data)
indices = np.where(arr == "")[0]
result = np.split(arr, indices + 1)
result = [list(x[x != ""]) for x in result]

def clean_data(data):
    def extract_numbers(item):
        return list(map(int, re.findall(r"[+-]?\d+", item)))
    result = np.array(data)
    vectorized_extract = np.vectorize(extract_numbers, otypes=[object])
    cleaned_data = vectorized_extract(result)
    return cleaned_data

# Cleaned data for further use
test_cleaned_data = clean_data(test_result)
cleaned_data = clean_data(result)

# Brute force solution to calculate least button presses
def calc_possibilities(num1, num2, total):
    #total = total
    valid_nums = set()
    x = 0
    y = 1
    while y >= 0.99:
        y = (total - (num1 * x)) / num2
        if y.is_integer():
            valid_nums.add((x, int(y)))
        x += 1
        #print(y)
    return valid_nums

# Calculate the values at intersection
def calc_whole_number(item):
    nums = 0
    num1 = item[0][0]
    num2 = item[1][0]
    total1 = item[2][0] + 10000000000000
    num3 = item[0][1]
    num4 = item[1][1]
    total2 = item[2][1] + 10000000000000
    x = -((total2*num2)-(total1*num4))/((num1*num4)-(num3*num2))
    y = (total1 - (num1 * x)) / num2
    if x.is_integer() and y.is_integer():
            nums = (int(x), int(y))
    return nums

# Get lowest from all button presses
def get_lowest(data):
    minimum = 0
    for value in data:
        total = (value[0] * 3) + (value[1] * 1)
        if minimum == 0:
            minimum = total
        elif minimum > total:
            minimum > total
    return minimum

# Brute force solution
def brutus_playmaker(data):
    total = 0
    for item in data:
        button_A = calc_possibilities(item[0][0], item[1][0], item[2][0])
        button_B = calc_possibilities(item[0][1], item[1][1], item[2][1])
        common_values = button_A.intersection(button_B)
        if len(common_values) != 0:
            total += get_lowest(common_values)
    return total

# More mathematical solution
def playmaker(data):
    total = 0
    for item in data:
        result = calc_whole_number(item)
        if result != 0:
            total += (result[0] * 3) + (result[1] * 1)
    return total


# Use for part 1
print(brutus_playmaker(test_cleaned_data))
print(brutus_playmaker(cleaned_data))

# Use for part 2
print(playmaker(test_cleaned_data))
print(playmaker(cleaned_data))