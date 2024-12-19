import pandas as pd


test_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

test_data = test_data.strip().split("\n")

test_rules = [value for value in test_data if "|" in value]

test_rule_list = [rule.split("|") for rule in test_rules]

test_df = pd.DataFrame(test_rule_list)

test_updates = [value.split(",") for value in test_data if "," in value]

print(test_df)

print(test_updates)



with open("aoc-day5-input.txt", "r") as file:
    data = file.read().strip().split("\n")

rules = [value for value in data if "|" in value]

rule_list = [rule.split("|") for rule in rules]

df = pd.DataFrame(rule_list)

updates = [value.split(",") for value in data if "," in value]


def countCorrect(df, updates):
    updateCount = 0
    correctCount = 0

    print(len(updates))

    for update in updates:
        print(update)
        print(updateCount)
        print(correctCount)
        for i in range(len(update)-1):
            emptiedList = update[i + 1:]
            for index, row in df.iterrows():
                if df.loc[index, 0] == update[i] and df.loc[index, 1] in emptiedList:
                    emptiedList.remove(df.loc[index, 1])
            if len(emptiedList) != 0:
                break
        updateCount += 1
        if len(emptiedList) != 0:
                continue
        correctCount += int(update[(len(update)-1)//2])

    return correctCount

def countIncorrect(df, updates):
    updateCount = 0
    incorrectCount = 0

    print("All", len(updates))

    for update in updates:
        print("\n")
        print(update)
        print("update count:", updateCount)
        print("total:", incorrectCount)
        for i in range(len(update)-1):
            emptiedList = update[i + 1:]
            for index, row in df.iterrows():
                if df.loc[index, 0] == update[i] and df.loc[index, 1] in emptiedList:
                    emptiedList.remove(df.loc[index, 1])
            if len(emptiedList) != 0:
                middle_value = makeCorrect(update, df)
                break

        updateCount += 1
        if len(emptiedList) != 0:
            print("fixed")
            incorrectCount += middle_value

    return incorrectCount


def makeCorrect(update, df):

    correctList = [None] * len(update)

    for i in range(len(update)):
        emptiedList = [x for x in update if x!= update[i]]
        for index, row in df.iterrows():
            if df.loc[index, 0] == update[i] and df.loc[index, 1] in emptiedList:
                emptiedList.remove(df.loc[index, 1])
        move_value = update[i]
        correctList[len(emptiedList)] = move_value

    middle_value = int(correctList[(len(update)-1)//2])

    return middle_value


#print(countCorrect(df, updates))

print(countIncorrect(df, updates))

#print(countIncorrect(test_df, test_updates))