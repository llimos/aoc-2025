from aocd import data

# data = """987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """

banks = data.splitlines()
total = 0
for bank in banks:
    max_first = 0
    max_second = 0
    max_first_index = None
    for i, cell in enumerate(bank):
        cell = int(cell)
        if i < len(bank) - 1 and cell > max_first:
            max_first = cell
            max_second = 0
            max_first_index = i
        elif cell > max_second:
            max_second = cell
    total += int(str(max_first) + str(max_second))
print(total)

# Part 2
total = 0
for bank in banks:
    current = [0] * 12
    for i, cell in enumerate(bank):
        cell = int(cell)
        for pos in range(0, 12):
            # Need another 11 - pos after it
            if i < len(bank) - (11 - pos):
                if cell > current[pos]:
                    current[pos] = cell
                    for reset_pos in range(pos + 1, 12):
                        current[reset_pos] = 0
                    break
    total += int(''.join([str(x) for x in current]))
print(total)
