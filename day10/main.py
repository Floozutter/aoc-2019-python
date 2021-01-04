INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
asteroids = frozenset(
	(i, j)
	for i, row in enumerate(raw.split())
	for j, char in enumerate(row)
	if char == "#"
)

from math import gcd
from typing import Tuple
def tuple_angle(di: int, dj: int) -> Tuple[int, int]:
	divisor = max(gcd(di, dj), 1)
	return di // divisor, dj // divisor
def detectable_asteroids(i: int, j: int) -> int:
	return len({tuple_angle(p - i, q - j) for p, q in asteroids}) - 1
(station_i, station_j), station_n = max(
	(((i, j), detectable_asteroids(i, j)) for i, j in asteroids),
	key = lambda pair: pair[1]
)
print(station_n)

from collections import defaultdict
stacks = defaultdict(list)
for i, j in asteroids:
	di, dj = i - station_i, j - station_j
	stacks[tuple_angle(di, dj)].append((di, dj))
del stacks[0, 0]
for stack in stacks.values():
	stack.sort(reverse = True)
from math import atan2, pi
def order_key(angle: Tuple[int, int]) -> float:
	i, j = angle
	theta = atan2(-i, j)
	return theta if theta > pi / 2 else theta + 2 * pi
order = sorted(stacks, key = order_key, reverse = True)
vaporized = []
while any(stacks.values()):
	for angle in order:
		if stack := stacks[angle]:
			vaporized.append(stack.pop())
di, dj = vaporized[199]
i, j = di + station_i, dj + station_j
print(j * 100 + i)
