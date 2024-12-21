from collections import defaultdict

# Test data
test_data = "125 17"
test_data = test_data.strip().split(" ")

# Actual data
with open("aoc-day11-input.txt", "r") as file:
    data = file.read().strip().split(" ")

# Transform a row of numbers
def transform_numbers(numbers):
    new_numbers = defaultdict(int)
    for number, count in numbers.items():
        if number == "0":
            new_numbers["1"] += count
        elif len(number) % 2 == 0:
            mid = len(number) // 2
            left = number[:mid]
            right = str(int(number[mid:]))
            new_numbers[left] += count
            new_numbers[right] += count
        else:
            transformed = str(int(number) * 2024)
            new_numbers[transformed] += count
    return new_numbers

# How many times transform or blink
def blink(data, count):
    numbers = defaultdict(int)
    for num in data:
        print(num)
        numbers[num] += 1

    for i in range(count):
        numbers = transform_numbers(numbers)
        print(i + 1)
    return sum(numbers.values())

#print(blink(test_data, 25))
print(blink(data, 75))
