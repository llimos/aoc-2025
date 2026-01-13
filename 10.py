from collections import Counter
from math import inf
from aocd import data, puzzle
from sympy import Symbol, solve

# data = puzzle.examples[0].input_data

# Parse
def parse(line):
    buttonsArray = line.split(' ')
    target = buttonsArray.pop(0)[1:-1]
    joltage = buttonsArray.pop()
    # Big-endian binary, basically
    target = sum([2**i for i, x in enumerate(target) if x == '#'])
    buttonsArray = [[int(y) for y in x[1:-1].split(',')] for x in buttonsArray]
    buttons = [sum([2**int(y) for y in x]) for x in buttonsArray]
    joltage = [int(x) for x in joltage[1:-1].split(',')]

    return {"target": target, "buttons": buttons, "buttonsArray": buttonsArray, "joltage": joltage}

data = [parse(line) for line in data.splitlines()]

# Order doesn't matter, neither do repeats
# bfs
def bfs(target, buttons, queue, pushes):
    next_queue = []
    for attempt in queue:
        new_val = attempt["val"] ^ buttons[attempt["button"]]
        if new_val == target:
            return pushes + 1
        next_queue.extend([{"val": new_val, "button": i} for i in range(attempt["button"] + 1, len(buttons))])
    if len(next_queue) == 0:
        return inf
    return bfs(target, buttons, next_queue, pushes + 1)

total = 0
for line in data:
    target = line["target"]
    if target == 0:
        continue
    buttons = line["buttons"]
    queue = [{"val": 0, "button": i} for i in range(len(buttons))]
    total += bfs(target, buttons, queue, 0)
print(total)

# Part 2
# Order still doesn't matter, but multiples do
# def joltageBfs(target_joltage, buttons, queue, pushes):
#     next_queue = []
#     for attempt in queue:
#         new_joltage: Counter = Counter(attempt["joltage"])
#         new_joltage.update(buttons[attempt["button"]])
#         # Check if we match
#         if new_joltage == target_joltage:
#             return pushes + 1
#         # Check if we busted
#         if any(new_joltage[i] > target_joltage[i] for i in range(len(new_joltage))):
#             continue
#         # Push to new queue. Include current button again
#         next_queue.extend([{"joltage": new_joltage, "button": i} for i in range(attempt["button"], len(buttons))])
#     print("finished step", pushes + 1)
#     if len(next_queue) == 0:
#         return inf
#     return joltageBfs(target_joltage, buttons, next_queue, pushes + 1)
#
#
#
# total = 0
# for i, line in enumerate(data):
#     print("Starting line", i)
#     target_joltage = Counter({i: x for i, x in enumerate(line["joltage"])})
#     buttons = line["buttonsArray"]
#     joltage = Counter({i: 0 for i in range(len(target_joltage))})
#     queue = [{"joltage": Counter({i: 0 for i in range(len(target_joltage))}), "button": i} for i in range(len(buttons))]
#     min = joltageBfs(target_joltage, buttons, queue, 0)
#     total += min
#     print("solved:", min)
# print(total)

# New attempt

# Global variable for current minimum
current_min: int|None = None

def get_min_pushes(
        joltage: list[int],
        buttons: list[Counter[int]],
        pushes: int):

    global current_min

    if sum(joltage) == 0:
        return 0
    if pushes > current_min:
        return inf
    # Find the joltage that the least number of buttons affects
    # target_joltage_index = min((x for x in range(len(joltage)) if joltage[x] > 0), key=lambda x: len([b for b in buttons_remaining if x in b]))
    # Find the smallest voltage, so we can do combos without checking for bust
    target_joltage_index = joltage.index(min(x for x in joltage if x > 0))
    # Buttons that affect it
    # Max pushes per button
    buttons_subset = [b for b in buttons if target_joltage_index in b]
    # Start making combinations of the results after zeroing the target joltage
    # print("Targeting", target_joltage_index, joltage[target_joltage_index])
    target = joltage[target_joltage_index]
    new_combos = button_combos(joltage, target, buttons_subset, pushes)
    pushes += target
    # print("combos", combos)
    # Recurse
    remaining_buttons = [x for x in buttons if x not in buttons_subset]
    min_pushes = inf
    for combo in new_combos:
        min_pushes = min(min_pushes, get_min_pushes(combo, remaining_buttons, pushes))
    # A combination also has a button push count
    # Repeat with the subset we have
    return target + min_pushes

# Returns a list of combos after one joltage has been zeroed
def button_combos(joltage, target, buttons, pushes) -> list[dict[str,Counter[int]|int]]:
    global current_min
    if target == 0 or len(buttons) == 0:
        return []
    if pushes + target >= current_min:
        return []
    # Start with the button that does the most at once
    button = max(buttons, key=lambda b: len(b))
    limit = min(joltage[x] for x in button)
    combos = []
    if limit == target:
        new_joltage = [x - (button[i] * target) for i, x in enumerate(joltage)]
        combos.append(new_joltage)
        if sum(joltage) == 0:
            current_min = min(current_min, pushes + target)
    if len(buttons) > 1: # There's where to provide the rest from
        for n in range(limit):
            # We've pushed the first button n times
            new_joltage = [x - (button[i] * n) for i, x in enumerate(joltage)]
            the_rest = button_combos(new_joltage, target - n, buttons[1:], pushes + n)
            combos.extend(x for x in the_rest if not any(v < 0 for v in x))
    return combos


# total = 0
# for line in data:
#     buttons = [Counter(x) for x in line["buttonsArray"]]
#     current_min = inf
#     res = get_min_pushes(line["joltage"], buttons, 0)
#     print(res)
#     total += res
# print("Grand Total", total)

# Third attempt
# Simultaneous equations
# for line in data[0:1]:
#     buttons = line['buttonsArray']
#     joltage = line['joltage']
#     # Build dict of which buttons affect which joltage
#     eqs = {i:[y for y in range(len(buttons)) if i in buttons[y]] for i,x in enumerate(joltage)}
#     print(eqs, joltage)
#     symbols = [Symbol('b'+str(x), real=True) for x in range(len(buttons))]
#     eqs = [sum([symbols[y] for y in range(len(buttons)) if i in buttons[y]]) - j for i,j in enumerate(joltage)]
#     # for symbol in symbols:
#     #     print(solve(eqs, [x for x in symbols if x != symbol], set=True))
#
#     # SymPy
#     root = solveset(eqs, symbols[0])
#     print(root)
#
#     # NumPy
#     a = np.array([[1 if i in b else 0 for b in buttons] for i,j in enumerate(joltage)])
#     b = np.array(joltage)
#     print(a, b)
#     res = np.linalg.lstsq(a, b)
#     print(res)

# Fourth attempt
# Based on subreddit
def divisible_by(joltage):
    # Only try from 5 down, fairly arbitrarily
    for n in (5, 4, 3, 2):
        if sum([x % n for x in joltage]) == 0:
            return n
    return None

def combos_to_even(joltage, buttons):
    results = []
    for buttonIndex, button in enumerate(buttons):
        new_joltage = [x - (1 if i in button else 0) for i,x in enumerate(joltage)]
        if min(new_joltage) < 0:
            continue
        if sum(new_joltage) == 0:
            return [[1, new_joltage]]
        if sum(x % 2 for x in new_joltage) == 0:
            results.append([1, new_joltage])
        for pushes, new_new_joltage in combos_to_even(new_joltage, buttons[buttonIndex+1:]):
            results.append([1 + pushes, new_new_joltage])
    return results


def steps(joltage, buttons):
    divide_by = divisible_by(joltage)
    if divide_by is not None:
        factor = divide_by
        joltage = [int(x / divide_by) for x in joltage]
        return steps(joltage, buttons) * factor
    combos = combos_to_even(joltage, buttons)
    min_pushes = inf
    for combo in combos:
        pushes, new_joltage = combo
        if sum(new_joltage) > 0:
            pushes += steps(new_joltage, buttons)
        min_pushes = min(pushes, min_pushes)
    return min_pushes

total = 0
for i, line in enumerate(data):
    joltage = line["joltage"]
    buttons = line["buttonsArray"]
    pushes = steps(joltage, buttons)
    if len(buttons) == len(joltage):
        # Use the simultaneous equations method
        symbols = [Symbol('b'+str(x), real=True) for x in range(len(buttons))]
        eqs = [sum([symbols[y] for y in range(len(buttons)) if i in buttons[y]]) - j for i,j in enumerate(joltage)]
        # for symbol in symbols:
        solution = solve(eqs, symbols, dict=True)
        print(solution)
        pushes = sum(solution[0].values())
    print(i, ':', pushes)
    total += pushes

print("Grand Total", total)
#135628 > x > 135633, not 15630