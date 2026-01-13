import math

from aocd import data

lines = data.splitlines()

# lines = """L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82
# """.splitlines()

dial = 50
zerocount = 0
zeroclicks = 0
for line in lines:
    dir = 1 if line[0] == "R" else -1
    amt = int(line[1:]) * dir
    dial = (dial + amt) % 100
    if dial == 0:
        zerocount += 1
    print("Move:", line, amt, "Dial:", dial, "Zeroes:", zerocount)
print(zerocount)

# Part 2
dial = 50
zerocount = 0
for line in lines:
    dir = 1 if line[0] == "R" else -1
    amt = int(line[1:]) * dir
    # Each 100 will include 1 zero
    zeroclicks = math.floor(abs(amt) / 100)
    # and the remainder
    if dial != 0:
        if (amt > 0 and dial + amt % 100 >= 100) or (amt < 0 and dial + amt % -100 <= 0):
            zeroclicks += 1
    zerocount += zeroclicks
    dial = (dial + amt) % 100
    print("Move:", line, amt, "Dial:", dial, "Zeroes:", zeroclicks)
print(zerocount)