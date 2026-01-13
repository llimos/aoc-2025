from functools import reduce

from aocd import data

# data = """3-5
# 10-14
# 16-20
# 12-18
#
# 1
# 5
# 8
# 11
# 17
# 32
# """

ranges, ids = data.split('\n\n')
ranges = [[int(y) for y in x.split('-')] for x in ranges.splitlines()]
ids = [int(x) for x in ids.splitlines()]

total = 0
for id in ids:
    for range in ranges:
        if range[0] <= id <= range[1]:
            total += 1
            break
print(total)

# Part 2
i = 0
ranges = sorted(ranges, key=lambda range: range[0])
while i < len(ranges):
    range = ranges[i]
    to_remove = list()
    for j, other_range in enumerate(ranges):
        if i == j:
            continue
        if other_range[0] - 1 <= range[0] <= other_range[1] + 1 or other_range[0] - 1 <= range[1] <= other_range[1] + 1:
            range[0] = min(range[0], other_range[0])
            range[1] = max(range[1], other_range[1])
            to_remove.append(j)
    removed = 0
    for k in to_remove:
        ranges.pop(k - removed)
        removed += 1
    i += 1
print(sorted(ranges, key=lambda range: range[0]), '\n')
print(reduce(lambda x, range: x + (1 + range[1] - range[0]), ranges, 0))