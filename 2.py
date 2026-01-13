from itertools import repeat
from math import floor

from aocd import data

# data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

ranges = [[int(y) for y in x.split('-')] for x in data.split(',')]

total = 0

for frm, to in ranges:
    while frm < to:
        # Split by number of digits
        frm_digits = len(str(frm))
        to_digits = len(str(to))
        if frm_digits % 2 == 1: # Odd digits can't be bad id
            frm = min(pow(10, frm_digits), to)
            continue
        # Even digits, start looking for bad ids
        current_to = min(pow(10, frm_digits), to)
        id_prefix = str(frm)[0:int(frm_digits/2)]
        current = int(id_prefix + id_prefix)
        if current < frm:
            id_prefix = str(int(id_prefix) + 1)
            current = int(id_prefix + id_prefix)
        while current <= current_to:
            print("Found", id_prefix + id_prefix)
            total += current
            id_prefix = str(int(id_prefix) + 1)
            current = int(id_prefix + id_prefix)
        frm = current_to
print(total)

# Part 2
total = 0
used = set()
for frm, to in ranges:
    print("Range", frm, to)
    while frm < to:
        frm_digits = len(str(frm))
        to_digits = len(str(to))
        current_to = min(pow(10, frm_digits), to)
        # Try any prefix that divides cleanly
        for i in range(1, floor(frm_digits / 2) + 1):
            if frm_digits % i == 0:
                id_prefix = str(frm)[0:i]
                current = int(id_prefix * int(frm_digits/i))
                while current < frm:
                    id_prefix = str(int(id_prefix) + 1)
                    current = int(id_prefix * int(frm_digits/i))
                while current <= current_to:
                    if current not in used:
                        print("Found", current)
                        total += current
                        used.add(current)
                    id_prefix = str(int(id_prefix) + 1)
                    current = int(id_prefix * int(frm_digits/i))
        frm = current_to
print(total)