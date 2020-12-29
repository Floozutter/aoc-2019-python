INPUTPATH = "input.txt"
#INPUTPATH = "input-test.txt"
with open(INPUTPATH) as ifile:
	raw = ifile.read()
path1, path2 = (line.split(",") for line in raw.strip().split())

from typing import Tuple, Iterable, Set, Dict
Point = Tuple[int, int]
directions = {"R": (1, 0), "U": (0, 1), "L": (-1, 0), "D": (0, -1)}
def take(path: Iterable[str]) -> Tuple[Set[Point], Dict[Point, int]]:
	points = set()
	steps = dict()
	x, y = 0, 0
	step = 0
	for move in path:
		dx, dy = directions[move[0]]
		for _ in range(int(move[1:])):
			x, y = x + dx, y + dy
			step += 1
			points.add((x, y))
			if (x, y) not in steps:
				steps[x, y] = step
	return points, steps
points1, steps1 = take(path1)
points2, steps2 = take(path2)
intersections = points1 & points2

print(min(map(lambda point: abs(point[0]) + abs(point[1]), intersections)))
print(min(map(lambda point: steps1[point] + steps2[point], intersections)))
