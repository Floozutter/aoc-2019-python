from collections import defaultdict

INPUTPATH = "input.txt"
#INPUTPATH = "input-test1.txt"
#INPUTPATH = "input-test2.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

orbits = list(lines.split())

sat = defaultdict(list)

for o in orbits:
    a, b = o.split(")")
    sat[a].append(b)


def count(d, v):
    #print(v)
    if any([bool(v in l) for l in d.values()]):
        for i,l in enumerate(d.values()):
            if v in l:
                key = list(d.keys())[i]
        return 1 + count(d, key)
    else:
        return 0


total = 0
for l in sat.values():
    for v in l:
        total += count(sat, v)
print(total)



g = defaultdict(set)

for o in orbits:
    a, b = o.split(")")
    g[a].add(b)
    g[b].add(a)


def countsearch(g, start, end):
    traversed = set()
    d = None
    def do(node, count=0):
        traversed.add(node)
        if node == end:
            nonlocal d
            d = count
        for v in g[node]:
            if v not in traversed:
                do(v, count + 1)
    do(start)
    return d - 2

print(countsearch(g, "YOU", "SAN"))
