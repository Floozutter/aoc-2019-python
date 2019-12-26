from functools import reduce
from itertools import tee
import re

INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"

with open(INPUTPATH) as ifile:
    lines = ifile.read().strip().split("\n")

def parse_moonstring(line):
    numstrs = re.findall(r"-?\d+\.?\d*", line)
    return (tuple(map(int, numstrs)), (0, 0, 0))

def add_tuples(a, b):
    return tuple(map(sum, zip(a, b)))

def apply_gravity(moonlist):
    moonlist = list(moonlist)
    def update(moon):
        def velchange(othermoon):
            posA = moon[0]
            posB = othermoon[0]
            return (1 if a < b else -1 if a > b else 0
                    for a, b in zip(posA, posB))
        total_dv = reduce(add_tuples, map(velchange, moonlist))
        return (moon[0], add_tuples(moon[1], total_dv))
    return map(update, moonlist)

def apply_velocity(moonlist):
    return ((add_tuples(moon[0], moon[1]), moon[1])
            for moon in moonlist)

def get_energy(moonlist):
    return sum(
            sum(map(abs, pos))*sum(map(abs, vel))
            for pos, vel in moonlist
            )

moons = map(parse_moonstring, lines)
for i in range(1000):
    moons = apply_gravity(moons)
    moons = apply_velocity(moons)
print(get_energy(moons))
