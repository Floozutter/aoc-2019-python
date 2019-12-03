INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

def getdata(filepath):
    with open(filepath) as ifile:
        lines = ifile.read()
    return [w for w in lines.split("\n")]

wirepaths = getdata(INPUTPATH)

wirepath_a = wirepaths[0].split(",")
wirepath_b = wirepaths[1].split(",")

grid_a = dict()
grid_b = dict()

def mark(grid, wirepath, char):
    already = []
    pos = (0, 0)
    steps = 0
    for segment in wirepath:
        direction = segment[0]
        dist = int(segment[1:])
        if direction == "R":
            diff = (1, 0)
        elif direction == "L":
            diff = (-1, 0)
        elif direction == "U":
            diff = (0, 1)
        elif direction == "D":
            diff = (0, -1)
        for i in range(dist):
            steps += 1
            pos = (pos[0] + diff[0], pos[1] + diff[1])
            if pos in grid and grid[pos] != char:
                already.append((pos, steps))
            else:
                grid[pos] = char
    return already

def taxicab(p):
    return abs(p[0]) + abs(p[1])

mark(grid_b, wirepath_b, "b")
hits_a = mark(grid_b, wirepath_a, "a")

print(min([taxicab(hit[0]) for hit in hits_b]))


mark(grid_a, wirepath_a, "a")
hits_b = mark(grid_a, wirepath_b, "b")

intersections = dict()
for hit in hits_a:
    intersections[hit[0]] = [hit[1], 0]
for hit in hits_b:
    intersections[hit[0]][1] = hit[1]

combined = []
for k, v in intersections.items():
    combined.append(v[0] + v[1])
print(min(combined))


