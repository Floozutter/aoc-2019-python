INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
from typing import NamedTuple, Tuple
class Moon(NamedTuple):
	pos: Tuple[int, int, int]
	vel: Tuple[int, int, int]
def line_to_pos(line: str) -> Tuple[int, int, int]:
	filtered = "".join(c for c in line if c.isdigit() or c in {"-", ","})
	return tuple(map(int, filtered.split(",")))
start = tuple(
	Moon(line_to_pos(line), (0, 0, 0))
	for line in raw.strip().split("\n")
)

from itertools import combinations
def step(moons: Tuple[Moon]) -> Tuple[Moon]:
	vels = tuple(list(moon.vel) for moon in moons)
	for i, j in combinations(range(len(moons)), 2):
		for axis, (a, b) in enumerate(zip(moons[i].pos, moons[j].pos)):
			if a < b:
				vels[i][axis] += 1
				vels[j][axis] -= 1
			elif a > b:
				vels[i][axis] -= 1
				vels[j][axis] += 1
	return tuple(
		Moon(tuple(map(sum, zip(moon.pos, vel))), vel)
		for moon, vel in zip(moons, vels)
	)

state = start
for _ in range(1000):
	state = step(state)
print(sum(
	sum(map(abs, moon.pos)) * sum(map(abs, moon.vel))
	for moon in state
))
