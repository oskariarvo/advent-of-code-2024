import itertools
import operator

test_data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

test_rows = test_data.strip().split("\n")
test_nums = [row.split() for row in test_rows]
test_results = [int(num[0][:-1]) for num in test_nums]
test_numbers = [num[1:] for num in test_nums]

with open("aoc-day7-input.txt", "r") as file:
    data = file.read().strip().split("\n")
rows = [line.split() for line in data]
results = [int(row[0][:-1]) for row in rows]
numbers = [row[1:] for row in rows]


def calibration(results, numbers, part):
    whole_total = 0
    if part == 2:
        ops = ["+", "*", "||"]
    elif part == 1:
        ops = ["+", "*"]
    operators = {
        "+": operator.add,
        "*": operator.mul,
        "||": lambda x, y: str(x) + str(y),
    }

    for i in range((len(numbers))):
        combinations = itertools.product(ops, repeat=(len(numbers[i]) - 1))
        combs = list(combinations)

        for comb in combs:
            total = 0
            cumuIdx = 0
            bIdx = 1
            total += int(numbers[i][cumuIdx])
            for op in comb:
                b = int(numbers[i][bIdx])
                if op == "||":
                    total = int(operators[op](total, b))
                else:
                    total = operators[op](total, b)
                cumuIdx += 1
                bIdx += 1
            if total == results[i]:
                whole_total += total
                break
    return whole_total

print(calibration(test_results, test_numbers, 1))
print(calibration(test_results, test_numbers, 2))

print(calibration(results, numbers, 1))
print(calibration(results, numbers, 2))
