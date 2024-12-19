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
        #print("\n")
        #print("index:", index)
        row = row.tolist()
        row = list(filter((-1).__ne__, row))
        #print("original:", row)
        for value in row:
            #print(ind, value)
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
                        #print(i)
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
        #print("overall:", isSafe)
        if isSafe == True:
            isSafeCount += 1
    
    return isSafeCount

def validate_row(row, v):
    #print("index:", v)
    new_row = row[:]
    new_row.pop(v)
    isSafeCount = False
    previous_value = new_row[0]
    new_row = list(filter((-1).__ne__, new_row))
    #print(new_row)
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
    #print(isSafeCount)

    return isSafeCount


def test_safe_count():
    # list1 = [3, 4, 2, 1, 3, 3]
    # list2 = [4, 3, 5, 3, 9, 3]
    # list3 = [3, 4, 2, 1, 3, 3]
    # list4 = [4, 3, 5, 3, 9, 3]
    # list5 = [3, 4, 2, 1, 3, 3]
    # list6 = [4, 3, 5, 3, 9, 3]
    #df = pd.DataFrame({"list1": list1, "list2": list2, "list3": list3, "list4": list4, "list5": list5, "list6": list6})
    data = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9]
    ]
    df = pd.DataFrame(data)
    #print(safe_count_part1(df))
    assert safe_count_part1(df) == 2
    assert safe_count_part2(df) == 4
    print(safe_count_part1(df))
    print(safe_count_part2(df))

test_safe_count()