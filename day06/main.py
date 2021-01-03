INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
from collections import defaultdict
satellites = defaultdict(set)
primaries = dict()
for orbit in raw.split():
	primary, satellite = orbit.split(")")
	satellites[primary].add(satellite)
	primaries[satellite] = primary

def orbit_count(primary: str, depth: int = 0) -> int:
	return depth + sum(orbit_count(s, depth + 1) for s in satellites[primary])
print(orbit_count("COM"))

from typing import Tuple
def ancestors(satellite: str) -> Tuple[str]:
	if (primary := primaries.get(satellite)) is not None:
		return (primary,) + ancestors(primary)
	else:
		return ()
from itertools import takewhile
def orbital_transfers(a: str, b: str) -> str:
	ancestors_a = ancestors(a)
	ancestors_b = ancestors(b)
	common = sum(1 for _ in takewhile(
		lambda pair: pair[0] == pair[1],
		zip(reversed(ancestors_a), reversed(ancestors_b))
	))
	return len(ancestors_a) + len(ancestors_b) - 2 * common
print(orbital_transfers("YOU", "SAN"))
