import pandas as pd

with open("aoc-day1-input.txt", "r") as file:
    data = file.read().strip().split("\n")

rows = [line.split() for line in data]

df = pd.DataFrame(rows, columns = ["list1", "list2"])

df["list1"] = df["list1"].astype(int)
df["list2"] = df["list2"].astype(int)


def total_distance(df):
    df["list1"] = sorted(df["list1"])
    df["list2"] = sorted(df["list2"])
    df_distance = df.diff(1,1).abs()
    return df_distance["list2"].sum()

print(total_distance(df))

def similarity_score(list1, list2):
    similarity_score = 0
    for value in list1:
        similarity_score += list2.value_counts().get(value, 0) * value
    return similarity_score

print(similarity_score(df["list1"], df["list2"]))
