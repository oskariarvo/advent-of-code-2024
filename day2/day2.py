import pandas as pd

def safe_count_part1(df):
    isSafeCount = 0
    for index, row in df.iterrows():
        previous_value = df.loc[index, 0]
        isInc = None
        isSafe = True
        for value in row:
            if (row[0] - row[1]) == 0:
                isSafe = False
                break

            if value == -1:
                break

            if isInc == None:
                if value > previous_value:
                    isInc = True
                elif value < previous_value:
                    isInc = False
            if isInc == True:
                if not (1 <= (value - previous_value) <= 3):
                    isSafe = False
            elif isInc == False:
                if not (1 <= (previous_value - value) <= 3):
                    isSafe = False
            previous_value = value
        if isSafe == True:
            isSafeCount += 1
    
    return isSafeCount

def safe_count_part2(df):
    isSafeCount = 0
    for index, row in df.iloc[:1000].iterrows():
        previous_value = df.loc[index, 0]
        isInc = None
        ind = 0
        isSafe = True
        print("\n")
        print("index:", index)
        row = row.tolist()
        row = list(filter((-1).__ne__, row))
        print("original:", row)
        for value in row:
            print(ind, value)
            if (row[0] - row[1]) == 0:
                if not (validate_row(row, 0) == True or (validate_row(row, 1)) == True):
                    isSafe = False
                break

            if value == -1:
                break

            if isInc == None:
                if value > previous_value:
                    isInc = True
                elif value < previous_value:
                    isInc = False
            if isInc == True:
                if not (1 <= (value - previous_value) <= 3):
                    isSafe = False
                    for i, va in enumerate(row, start=0):
                        print(i)
                        if validate_row(row, i) == True:
                            isSafe = True
                            break
                    break
            elif isInc == False:
                if not (1 <= (previous_value - value) <= 3):
                    isSafe = False
                    for i, va in enumerate(row, start=0):
                        if validate_row(row, i) == True:
                            isSafe = True
                            break
                    break
            previous_value = value
            ind += 1
        print("overall:", isSafe)
        if isSafe == True:
            isSafeCount += 1
    
    return isSafeCount

def validate_row(row, v):
    print("index:", v)
    new_row = row[:]
    new_row.pop(v)
    isSafeCount = False
    previous_value = new_row[0]
    new_row = list(filter((-1).__ne__, new_row))
    print(new_row)
    isInc = None
    isSafe = True
    for value in new_row:
        if (new_row[0] - new_row[1]) == 0:
            isSafe = False
            break
        if isInc == None:
            if value > previous_value:
                isInc = True
            elif value < previous_value:
                isInc = False
        if isInc == True:
            if not (1 <= (value - previous_value) <= 3):
                isSafe = False
        elif isInc == False:
            if not (1 <= (previous_value - value) <= 3):
                isSafe = False
        previous_value = value
    if isSafe == True:
        isSafeCount = True
    print(isSafeCount)

    return isSafeCount




with open("aoc-day2-input.txt", "r") as file:
    data = file.read().strip().split("\n")

rows = [line.split() for line in data]

df = pd.DataFrame(rows)

df.fillna("-1", inplace = True)

df = df.astype(int, False)

print(safe_count_part1(df))

print(safe_count_part2(df))
