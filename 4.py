from aocd import data

# data = """..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.
# """

lines = [list(x) for x in data.splitlines()]

oldtotal = 0
total = 0
while True:
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '@':
                surrounding = 0
                for testy in range (y-1, y+2):
                    if testy < 0 or testy >= len(lines[y]):
                        continue
                    for testx in range(x-1, x+2):
                        if testx < 0 or testx >= len(lines[y]) or (testy == y and testx == x):
                            continue
                        if lines[testy][testx] == '@':
                            surrounding += 1
                            if surrounding == 4:
                                break
                    if surrounding == 4:
                        break
                else:
                    print(y, x)
                    lines[y][x] = 'x'
                    total += 1
    if oldtotal == total:
        break
    else:
        oldtotal = total
print(total)
