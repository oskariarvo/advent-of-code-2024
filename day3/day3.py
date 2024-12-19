import re

with open("aoc-day3-input.txt", "r") as file:
    data = file.read().strip().split("\n")

def mul_it_over(data):

    mul_list = []
    for value in data:
        parsed = re.findall(r"(mul\(\d+,\d+\))" , value)
        for mul in parsed:
            mul_list.append(mul)

    the_sum = 0

    for calc in mul_list:
        nums = re.findall(r"(\d+)", calc)
        the_sum += (int(nums[0]) * int(nums[1]))

    return the_sum

def mul_it_over_condition(data):

    mul_list = []
    for value in data:
        parsed = re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))" , value)
        for mul in parsed:
            mul_list.append(mul)
            
    the_sum = 0
    do_calc = True

    for calc in mul_list:
        nums = re.findall(r"(\d+|do\(\)|don't\(\))", calc)
        if (nums[0] == "do()"):
            do_calc = True
        elif (nums[0] == "don't()"):
            do_calc = False
        if do_calc == True and len(nums) == 2:
            the_sum += (int(nums[0]) * int(nums[1]))

    return the_sum

print(mul_it_over(data))
print(mul_it_over_condition(data))

print(mul_it_over(data)-mul_it_over_condition(data))