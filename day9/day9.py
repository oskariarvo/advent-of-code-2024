import itertools

# Test data
test_data = "2333133121414131402"
test_data = test_data.strip()

# Actual data
with open("aoc-day9-input.txt", "r") as file:
    data = file.read().strip()

# Calculate the ids and blocks
def disk_map_with_dots(data):
    data = list(data)
    id_count = 0
    current = 0
    new_data = []
    for character in data:
        if current % 2 == 0:
            new_data.extend([id_count] * int(character))
            id_count += 1
        else:
            new_data.extend(["."] * int(character))
        current += 1
    return new_data

# Trim disk map / more blocks from right to left
def trim_disk_map(data):
    rightmost_block = len(data) - 1
    char_count = len(data) - data.count(".")
    while (data.index(".") != char_count):
        leftmost_dot = data.index(".")
        # Skip if there is a dot at the end
        if data[rightmost_block] == ".":
            rightmost_block -= 1
            continue
        data[leftmost_dot] = data[rightmost_block]
        data[rightmost_block] = "."
        rightmost_block -= 1
    return data

# Calculate the checksum
def count_checksum(data):
    count = 0
    each_digit = 0
    for character in data:
        if character == ".":
            continue
        count += int(character) * each_digit
        each_digit += 1
    return count

def disk_fragmenter_part1(data):
    dots_data = disk_map_with_dots(data)
    trimmed_data = trim_disk_map(dots_data)
    return count_checksum(trimmed_data)




# Calculate the ids IN blocks
def disk_map_in_blocks(data):
    data = list(data)
    id_count = 0
    current = 0
    new_data = []
    for character in data:
        if current % 2 == 0:
            new_data.append([id_count] * int(character))
            id_count += 1
        else:
            new_data.append(["."] * int(character))
        current += 1
    return new_data

# Trim disk map / more blocks from right to left
def trim_disk_blocks(data):
    data = [value for value in data if value != []]
    characters = [value for value in data if "." not in value]
    reversed_data = characters[::-1]
    # Iterate over every id on reverse order
    for items in reversed_data:
        rightmost_block = data.index(items)
        rightmost_block_count = len(data[rightmost_block])
        dots = [i for i, value in enumerate(data) if "." in value]
        # Iterate over every dot before the id, if found -> replace
        for index in dots:
            if index > rightmost_block:
                break
            leftmost_dot_count = len(data[index])
            if rightmost_block_count <= leftmost_dot_count:
                difference = leftmost_dot_count - rightmost_block_count
                data[index] = data[rightmost_block]
                data[rightmost_block] = ["."] * rightmost_block_count
                if difference != 0:
                    data.insert(index + 1, ["."] * difference)
                break
    # Make the whole messy nested list into a one clean list
    data = list(itertools.chain.from_iterable(data))
    return data

# Calculate the new checksum
def count_new_checksum(data):
    count = 0
    each_digit = -1
    for character in data:
        each_digit += 1
        if character == ".":
            continue
        count += int(character) * each_digit
    return count

def disk_fragmenter_part2(data):
    dots_data = disk_map_in_blocks(data)
    trimmed_data = trim_disk_blocks(dots_data)
    return count_new_checksum(trimmed_data)




print(disk_fragmenter_part1(test_data))
print(disk_fragmenter_part1(data))

print(disk_fragmenter_part2(test_data))
print(disk_fragmenter_part2(data))