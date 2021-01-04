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
def angle(di: int, dj: int) -> Tuple[int, int]:
	divisor = max(gcd(di, dj), 1)
	return di // divisor, dj // divisor
def detectable_asteroids(i: int, j: int) -> int:
	return len({angle(p - i, q - j) for p, q in asteroids}) - 1
print(max(detectable_asteroids(i, j) for i, j in asteroids))
