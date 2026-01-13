from functools import reduce

from aocd import data

# data = """123 328  51 64
#  45 64  387 23
#   6 98  215 314
# *   +   *   +
# """

lines = data.splitlines()
ops = lines.pop().split()
linenums = [[int(y) for y in x.split()] for x in lines]

total = 0
for i, op in enumerate(ops):
    if op == '+':
        total += reduce(lambda acc, x: acc + x[i], linenums, 0)
    else:
        total += reduce(lambda acc, x: acc * x[i], linenums, 1)
print(total)

# Part 2
total = 0
linechars = [list(x) for x in lines]
while len(ops):
    op = ops.pop()
    subtotal = 1 if op == '*' else 0
    while len(linechars[0]):
        num_string = ''.join([x.pop() for x in linechars]).strip()
        if num_string == '':
            break
        subtotal = subtotal * int(num_string) if op == '*' else subtotal + int(num_string)
    total += subtotal
print(total)
