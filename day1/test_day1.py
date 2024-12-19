import pandas as pd

def total_distance(df):
    df["list1"] = sorted(df["list1"])
    df["list2"] = sorted(df["list2"])
    df_distance = df.diff(1,1).abs()
    return df_distance["list2"].sum()

def test_total_distance():
    list1 = [3, 4, 2, 1, 3, 3]
    list2 = [4, 3, 5, 3, 9, 3]
    df = pd.DataFrame({"list1": list1, "list2": list2})
    assert total_distance(df) == 11

def similarity_score(list1, list2):
    similarity_score = 0
    for value in list1:
        similarity_score += list2.value_counts().get(value, 0) * value
    return similarity_score

def test_similarity_score():
    list1 = [3, 4, 2, 1, 3, 3]
    list2 = [4, 3, 5, 3, 9, 3]
    df = pd.DataFrame({"list1": list1, "list2": list2})
    assert similarity_score(df["list1"], df["list2"]) == 31