from aocd import data

data = data.split('\n\n')
puzzles = data.pop()
shapes = [len([y for y in x if y == '#']) for x in data]
puzzles = [{'area': int(x[0:2])*int(x[3:5]), 'shapes': [int(y) for y in x[7:].split(' ')]} for x in puzzles.splitlines()]
success = 0
for puzzle in puzzles:
    shape_area = sum(n * shapes[i] for i,n in enumerate(puzzle['shapes']))
    if shape_area <= puzzle['area']:
        success += 1
print(success)