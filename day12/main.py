import re

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read()

data = lines.strip().split("\n")
data = [list(map(int, re.findall(r"-?\d+\.?\d*", s))) for s in data]

class Moon:
    def __init__(self, postuple):
        self.x, self.y, self.z = postuple
        self.vx, self.vy, self.vz = (0, 0, 0)

def printmoons(moonlist):
    for moon in moons:
        print("(", moon.x, moon.y, moon.z, ")",
              "(", moon.vx, moon.vy, moon.vz, ")")
        
moons = [Moon((d[0], d[1], d[2])) for d in data]

def timestep(moonlist):
    # gravity
    matched = set()
    for i, moon in enumerate(moonlist):
        for j, othermoon in enumerate(moonlist):
            if i == j:
                continue
            if ((i, j) in matched) or ((j, i) in matched):
                continue
            if moon.x > othermoon.x:   
                moon.vx -= 1
                othermoon.vx += 1
            elif moon.x < othermoon.x:
                moon.vx += 1
                othermoon.vx -= 1
            if moon.y > othermoon.y:
                moon.vy -= 1
                othermoon.vy += 1
            elif moon.y < othermoon.y:
                moon.vy += 1
                othermoon.vy -= 1
            if moon.z > othermoon.z:
                moon.vz -= 1
                othermoon.vz += 1
            elif moon.z < othermoon.z:
                moon.vz += 1
                othermoon.vz -= 1
            matched.add((i, j))
    # velocity
    for moon in moonlist:
        moon.x += moon.vx
        moon.y += moon.vy
        moon.z += moon.vz

def energy(moon):
    pot = abs(moon.x) + abs(moon.y) + abs(moon.z)
    kin = abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
    return pot * kin

for i in range(1000):
    timestep(moons)

print(sum(map(energy, moons)))


moons = [Moon((d[0], d[1], d[2])) for d in data]
def staterepr(moonlist):
    out = ""
    for moon in moonlist:
        out+= ",".join(map(str, (moon.x, moon.y, moon.z))) + " "
        out+= ",".join(map(str, (moon.vx, moon.vy, moon.vz))) + "\n"
    return out

states = set()
i = 0
while True:
    if i % 100000 == 0:
        print(i)
    s = staterepr(moons)
    if s in states:
        break
    states.add(s)
    timestep(moons)
    i += 1
print(i)
