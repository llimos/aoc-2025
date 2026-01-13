from math import sqrt

from aocd import data

# data="""162,817,812
# 57,618,57
# 906,360,560
# 592,479,940
# 352,342,300
# 466,668,158
# 542,29,236
# 431,825,988
# 739,650,466
# 52,470,668
# 216,146,977
# 819,987,18
# 117,168,530
# 805,96,715
# 346,949,466
# 970,615,88
# 941,993,340
# 862,61,35
# 984,92,344
# 425,690,689
# """

data = [[int(y) for y in x.split(',')] for x in data.splitlines()]

def distance(p1, p2):
    [x1, y1, z1] = p1
    [x2, y2, z2] = p2
    return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

bydistance = list()
for i, p1 in enumerate(data):
    for j in range(i+1, len(data)):
        p2 = data[j]
        bydistance.append({"nodes": [i, j], "distance": distance(p1, p2)})

bydistance.sort(key=lambda x: x["distance"])
# print(bydistance)
# print([{"d":x["distance"], "n":[data[y] for y in x["nodes"]]} for x in bydistance])

circuits = [{x} for x in range(len(data))]
circuits_by_node = {x: circuits[x] for x in range(len(data))}

for i in range(1000):
    # Join the nodes in bydistance[i]
    node1 = bydistance[i]["nodes"][0]
    node2 = bydistance[i]["nodes"][1]
    circuit1 = circuits_by_node[node1]
    circuit2 = circuits_by_node[node2]
    if circuit1 == circuit2:
        continue
    circuit1.update(circuit2)
    circuits.remove(circuit2)
    for n in circuit2:
        circuits_by_node[n] = circuit1

circuits.sort(key=lambda x: len(x), reverse=True)
print(circuits)
print([len(x) for x in circuits])
print(len(circuits[0])*len(circuits[1])*len(circuits[2]))

# Part 2

circuits = [{x} for x in range(len(data))]
circuits_by_node = {x: circuits[x] for x in range(len(data))}

for entry in bydistance:
    # Join the nodes in bydistance[i]
    node1 = entry["nodes"][0]
    node2 = entry["nodes"][1]
    circuit1 = circuits_by_node[node1]
    circuit2 = circuits_by_node[node2]
    if circuit1 == circuit2:
        continue
    circuit1.update(circuit2)
    circuits.remove(circuit2)
    for n in circuit2:
        circuits_by_node[n] = circuit1
    if len(circuits) == 1:
        print(data[node1][0] * data[node2][0])
        break
