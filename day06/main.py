INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
from collections import defaultdict
orbits = defaultdict(set)
for orbit in raw.split():
	primary, satellite = orbit.split(")")
	orbits[primary].add(satellite)

def orbit_count(primary: str, depth: int = 0) -> int:
	return depth + sum(orbit_count(s, depth + 1) for s in orbits[primary])
print(orbit_count("COM"))
