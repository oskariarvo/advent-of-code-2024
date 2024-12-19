import re

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

def test_mul_it_over():
    assert mul_it_over(["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]) == 161
    assert mul_it_over_condition(["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]) == 48