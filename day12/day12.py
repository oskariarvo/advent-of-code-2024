import pandas as pd

grid = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

# Making test data into dataframe
chars = grid.strip().split("\n")
eachchars = [list(row) for row in chars]
pf = pd.DataFrame(eachchars)

# Making actual data into dataframe
with open("aoc-day12-input.txt", "r") as file:
    data = file.read().strip().split("\n")
rows = [list(line) for line in data]
df = pd.DataFrame(rows)

# Using flood fill to find an area
def flood_fill_df(df, start, target):
    stack = [start]
    visited = set()
    region = []
    while stack:
        row, col = stack.pop()
        if (row, col) in visited:
            continue
        visited.add((row, col))
        region.append((row, col))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(df) and 0 <= nc < len(df.columns):
                if (nr, nc) not in visited and df.loc[nr, nc] == target:
                    stack.append((nr, nc))

    return region

# Find all areas
def check_all(df):
    coords = []
    y = -1
    for index, row in df.iterrows():
        y += 1
        x = -1
        for value in row:
            x += 1
            found = any((y, x) in row for row in coords)
            if found == False:
                coords.append(flood_fill_df(df, (y, x), df.loc[(y, x)]))
    return coords

# Count the perimeter of an area
def count_perimeter(area):
    total = 0
    for plant in area:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = plant[0] + dr, plant[1] + dc
            if (nr, nc) not in area:
                total += 1
    return total

# Count the prices
def count_prices(pf):
    all_areas = check_all(pf)
    total = 0
    for area in all_areas:
        perimeter = count_perimeter(area)
        region = len(area)
        price = perimeter * region
        total += price
    return total

# Counting the sides is the same as counting corners since: corners == sides
def count_sides(area):
  edges = 0
  for (r, c) in area:
    north_neighbor = (r - 1, c)
    west_neighbor = (r, c - 1)
    nw_neighbor = (r - 1, c - 1)
    if (north_neighbor not in area):
      same_edge = (west_neighbor in area) and (nw_neighbor not in area)
      if not same_edge:
        edges += 1

    south_neighbor = (r + 1, c)
    sw_neighbor = (r + 1, c - 1)
    if south_neighbor not in area:
      same_edge = (west_neighbor in area) and (sw_neighbor not in area)
      if not same_edge:
        edges += 1

    if west_neighbor not in area:
      same_edge = (north_neighbor in area) and (nw_neighbor not in area)
      if not same_edge:
        edges += 1

    east_neighbor = (r, c + 1)
    ne_neighbor = (r - 1, c + 1)
    if east_neighbor not in area:
      same_edge = (north_neighbor in area) and (ne_neighbor not in area)
      if not same_edge:
        edges += 1
  return edges

# Count the discount price using the areas sides/corners
def count_discount_prices(pf):
    all_areas = check_all(pf)
    total = 0
    for area in all_areas:
        sides = count_sides(area)
        region = len(area)
        price = sides * region
        total += price
    return total

#print(count_prices(pf))
print(count_prices(df))

#print(count_discount_prices(pf))
print(count_discount_prices(df))