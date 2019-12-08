INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read().strip()

wirepaths = lines.split("\n")
pathA = wirepaths[0].split(",")
pathB = wirepaths[1].split(",")

def follow(wirepath):
    DIRECTIONS = {
            "L" : (-1, 0),
            "R" : (+1, 0),
            "U" : (0, +1),
            "D" : (0, -1)
            }
    pos = (0, 0)
    stepcount = 0
    visited = set()
    steps = dict()
    for s in wirepath:
        delta = DIRECTIONS[s[0]]
        dist = int(s[1:])
        for i in range(dist):
            stepcount += 1
            pos = (pos[0] + delta[0], pos[1] + delta[1])
            visited.add(pos)
            if pos not in steps:
                steps[pos] = stepcount
    return visited, steps

def taxicab(p):
    return abs(p[0]) + abs(p[1])

visitsA, stepsA = follow(pathA)
visitsB, stepsB = follow(pathB)
intersections = visitsA & visitsB

print(min(map(taxicab, intersections)))
print(min(stepsA[i] + stepsB[i] for i in intersections))


