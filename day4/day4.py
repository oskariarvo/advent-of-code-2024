import pandas as pd

grid = "MMMSXXMASM", "MSAMXMSMSA", "AMXSXMAAMM", "MSAMASMSMX", "XMASAMXAMM", "XXAMMXXAMA", "SMSMSASXSS", "SAXAMASAAA", "MAMMMXMMMM", "MXMXAXMASX"

with open("aoc-day4-input.txt", "r") as file:
    data = file.read().strip().split("\n")

rows = [list(line) for line in data]

chars = [list(row) for row in grid]

#print(chars)

df = pd.DataFrame(rows)

pf = pd.DataFrame(chars)

#test_df = pd.DataFrame(chars)

#print(df)
def word_count(target, df):
    directions = [
        (0, 1), # oikealle
        (0, -1), # vasemmalle
        (-1, 0), # ylöspäin
        (1, 0), # alaspäin
        (1, 1), # oikea yläkulma
        (1, -1), # vasen yläkulma
        (-1, 1), # oikea alakulma
        (-1, -1) # vasen alakulma
    ]

    word_count = 0

    def validate(df, index, i, direction, word_len):
        for k in range(word_len):
            ni, nj = index + k * direction[0], i + k * direction[1]
            if not (0 <= ni < len(df) and 0 <= nj < len(df.columns)):
                return False
            if df.loc[ni, nj] != target[k]:
                return False
        return True

    for index, row in df.iterrows():
        for i, value in enumerate(row.tolist()):
            if value == target[0]:
                for direction in directions:
                    if validate(df, index, i, direction, len(target)):
                        word_count += 1
    return word_count


def word_X_count(target, df):

    word_count = 0

    def validate(df, index, i, word_len):
        directions = [
        (-1, 1), # oikea yläkulma
        (1, -1), # vasen alakulma
        (-1, -1), # vasen yläkulma
        (1, 1) # oikea alakulma
    ]
        current = ""
        for direction in directions:
            ni, nj = index + direction[0], i + direction[1]
            #print(ni, nj)
            if not (0 <= ni < len(df) and 0 <= nj < len(df.columns)):
                return False
            #print(direction)
            #print(df.loc[ni, nj])
            if not (df.loc[ni, nj] == target[2:] or df.loc[ni, nj] == target[:1]):
                return False
            if (direction == (1, -1) or direction == (1, 1)) and current == df.loc[ni, nj] :
                return False
            current = df.loc[ni, nj]
        return True

    for index, row in df.iterrows():
        for i, value in enumerate(row.tolist()):
            if value == target[1]:
                #print("\n")
                #print(index, i, value)
                if validate(df, index, i, len(target[2:])):
                    #print("truu")
                    word_count += 1
                    #print("\n")
    return word_count



print("Total XMAS count:", word_count("XMAS", df))
print("Total X-MAS count:", word_X_count("MAS", df))