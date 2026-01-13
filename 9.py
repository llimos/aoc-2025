from math import inf

from aocd import data
from aocd import puzzle

# data = puzzle.examples[0].input_data
data = [[int(y) for y in x.split(',')] for x in data.splitlines()]

max_area = 0
for i in range(len(data) - 1):
    for j in range(i+1, len(data)):
        x1,y1 = data[i]
        x2,y2 = data[j]
        area = abs(1+x1-x2) * abs(1+y1-y2)
        if area > max_area:
            max_area = area
print(max_area)

# Part 2
row_left = dict()
row_right = dict()
col_top = dict()
col_bottom = dict()

# List loop-around
data.append(data[0])

# Build map of edges
for i in range(len(data) - 1):
    x1, y1 = data[i]
    x2, y2 = data[i + 1]
    if x1 == x2:
        # Moving up/down
        x = x1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            row_left[y] = min(row_left.get(y, inf), x)
            row_right[y] = max(row_right.get(y, 0), x)
    elif y1 == y2:
        # Moving left/right
        y = y1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            col_top[x] = min(col_top.get(x, inf), y)
            col_bottom[x] = max(col_bottom.get(x, 0), y)
    else:
        raise Exception("should not happen")

# Re-remove loop-around
data.pop()

# print('left  ', row_left)
# print('right ', row_right)
# print('top   ', col_top)
# print('bottom', col_bottom)

def validate(p1, p2):
    x1 = min(p1[0], p2[0])
    x2 = max(p1[0], p2[0])
    y1 = min(p1[1], p2[1])
    y2 = max(p1[1], p2[1])
    # Validate each point along edges
    # Top - x1,y1 to x2,y1 and bottom x1,y2 to x2,y2
    for x in range(x1, x2 + 1):
        if y1 < col_top[x] or y2 > col_bottom[x]:
            return False
    # Left - x1,y1 to x2,y1 and right x2,y1 to x2,y2
    for y in range(y1, y2 + 1):
        if x1 < row_left[y] or x2 > row_right[y]:
            return False
    return True

max_area = 0
for i in range(len(data) - 1):
    for j in range(i+1, len(data)):
        if not validate(data[i], data[j]):
            continue
        x1,y1 = data[i]
        x2,y2 = data[j]
        area = (abs(x1-x2)+1) * (abs(y1-y2)+1)
        if area > max_area:
            max_area = area
print(max_area)