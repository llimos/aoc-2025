from aocd import data

# data = """.......S.......
# ...............
# .......^.......
# ...............
# ......^.^......
# ...............
# .....^.^.^.....
# ...............
# ....^.^...^....
# ...............
# ...^.^...^.^...
# ...............
# ..^...^.....^..
# ...............
# .^.^.^.^.^...^.
# ...............
# """

lines = [list(x) for x in data.splitlines()]
flowing = {lines[0].index('S')}
splitters = 0
for line in lines[1:]:
    newflowing = set()
    for flow in flowing:
        if line[flow] == '^':
            splitters += 1
            if flow > 0:
                newflowing.add(flow - 1)
            if flow < len(line) - 1:
                newflowing.add(flow + 1)
        else:
            newflowing.add(flow)
    flowing = newflowing
print(splitters)

# Part 2
cache = dict()
def dfs(y, x):
    if y == len(lines):
        return 1
    if lines[y][x] == '.':
        return dfs(y+1, x)
    cachekey = str(y) + '-' + str(x)
    if cachekey in cache:
        return cache[cachekey]
    res = dfs(y+1, x-1) + dfs(y+1, x+1)
    cache[cachekey] = res
    return res
print(dfs(1, lines[0].index('S')))