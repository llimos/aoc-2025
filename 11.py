from collections import Counter

from aocd import data, puzzle

connections = {x.split(':')[0]:x.split(':')[1].strip().split(' ') for x in data.splitlines()}
print(connections)

cache = dict()
def paths(start: str) -> dict[str,int]:
    if start in cache:
        return cache[start]
    counts = Counter({
        'with_dac': 0,
        'with_fft': 0,
        'with_dac_fft': 0,
        'without_dac_fft': 0,
    })
    if start == 'out':
        counts['without_dac_fft'] = 1
        return counts
    for path in connections[start]:
        path_count = paths(path)
        if start == 'dac':
            counts['with_dac'] += path_count['with_dac'] + path_count['without_dac_fft']
            counts['with_dac_fft'] += path_count['with_dac_fft'] + path_count['with_fft']
        elif start == 'fft':
            counts['with_fft'] += path_count['with_fft'] + path_count['without_dac_fft']
            counts['with_dac_fft'] += path_count['with_dac_fft'] + path_count['with_dac']
        else:
            counts += path_count

    cache[start] = counts
    return counts

print(paths('svr')['with_dac_fft'])